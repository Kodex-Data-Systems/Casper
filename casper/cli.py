import subprocess, os, pprint, time, requests
from .utils import get_exec_sh
class Cli(object):
    def __init__(self, settings):
        self.node = settings["node"]
        self.storage = settings["jmpath"]
        self.loaded = True
        self.genesis = settings["genesis"]
        self.executable = get_exec_sh()

        if "NO_JORMUNGANDR" in settings:
            self.no_jormungandr = settings["NO_JORMUNGANDR"]
        else:
            self.no_jormungandr = False

    def _run(self, runstring, errorstring=None):

        try:
            output = subprocess.check_output(
                str(runstring),
                shell=True,
                executable=self.executable
            ).decode()

            if output.find("failed to make a REST request") < -1:
                return
            return output.replace("\n", "")

        except subprocess.CalledProcessError:
            if errorstring is None:
                print(f'Error running command: {runstring}\n')
            else:
                print(str(errorstring))

    def prefix(self, prefix, priv_key):
        return self._run(
            f'jcli address account --prefix "{prefix}" --testing {priv_key}',
            "error cli.prefix"
        ).replace("\n", "")

    def show_jcli_version(self):
        return self._run("jcli --full-version").replace("\n", "")

    def show_jormungandr_version(self):
        try:
            return self._run(
                'jormungandr --full-version',
                "error cli.show_jormungandr_version"
            ).replace("\n", "")
        except:
            return None

    def show_blockchain_size(self):
        try:
            return self._run(
                f'ls -lrth {self.storage}',
                "error cli.show_blockchain_size"
            )
        except:
            return None

    def show_stake(self):
        #  moved into node module
        return self._run(
            f'jcli rest v0 stake get -h {self.node}/api',
            "error cli.show_stake"
        )

    def show_stake_pools(self):
        return self._run(
            f'jcli rest v0 stake-pools get -h {self.node}/api',
            "error cli.show_stake_pools"
        )

    def show_balance(self, acct_addr, raw=True):
        try:
            raw_output = self._run(
                f'jcli rest v0 account get {acct_addr} -h {self.node}/api',
                'Unable to view balance, account has not yet received a tx or node is offline.'
            )

            if raw is True:
                return raw_output
            else:
                balance = str(raw_output).split("value: ")
                balance = balance[1]
                counter = raw_output.split("counter: ")[1].split("delegation:")[0]
                counter = int(counter)
                return acct_addr, balance, counter

        except Exception as e:
            print(e)
            return 0

    def message_logs(self, parse=False):
        raw = self._run(
            f'jcli rest v0 message logs -h {self.node}/api',
            "error message logs"
        )
        try:
            raw = raw.replace("---\n", "")
            split = raw.split("\n-")
            logs = []

            for elem in split:
                obj = {
                    "fragment_id": elem.split("fragment_id: ")[1].split("\n")[0],
                    "last_updated_at": elem.split("last_updated_at: ")[1].split("\n")[0],
                    "received_at": elem.split("received_at: ")[1].split("\n")[0],
                    "received_from": elem.split("received_from: ")[1].split("\n")[0],
                    "date": elem.split(': "')[1].replace('"', "").split("\n")[0],
                }

                logs.append(obj)

            if parse is not False:
                return logs
            return raw
        except:
            return

    def genesis_decode(self):
        decoded_genesis = self._run(
            f"curl -s {self.node}/api/v0/block/{self.genesis} | jcli genesis decode"
        )
        return decoded_genesis

    def create_acct(self):
        ''' Create Secret Key, Public Key and Account Address '''

        #  Generate secret using JCLI.
        _new_secret = self._run(
            'jcli key generate --type ed25519extended',
            "error generating secret"
        ).replace("\n", "")

        return self.acct_by_secret(_new_secret)

    def acct_by_secret(self, secret):#
        ''' Get account details by secret key '''
        #  echo system call can not generate required result, save result to file instead.
        os.system('echo ' + secret + ' | jcli key to-public > p.tmp')
        with open('p.tmp', 'r') as f:
            _new_public = f.read()[:-1]
        os.remove('p.tmp')

        #  Generate account using JCLI.
        _new_acct = self._run(
            f'jcli address account {_new_public} --testing',
            "error generating account"
        ).replace("\n", "")

        return secret, _new_public, _new_acct

    def _remove_tmp(self):
        try:
            os.remove('witness.output.tmp')
            os.remove('witness.secret.tmp')
            os.remove('file.staging')
            os.remove('stake_pool.cert')
            os.remove('stake_pool.signcert')

        except:
            return False


################## Certs ##################################
    def _get_cert(self):
        try:
            get_fee = requests.get(f"{self.node}/api/v0/settings").json()
            cert = get_fee['fees']['certificate']
            return cert
        except:
            return False

    def create_pool(self, pk, sk, account, pool_name):
        #  1 Create VRF Secret
        _pool_vrf_sk = subprocess.check_output(
            f'jcli key generate --type Curve25519_2HashDH',
            shell=True,
            executable=self.executable
        ).decode()[:-1]

        os.system(f'echo {_pool_vrf_sk} | jcli key to-public > p.tmp')

        with open('p.tmp', 'r') as f:
            _pool_vrf_pk = f.read()[:-1]
        os.remove('p.tmp')

        #  2 Create KES Secret
        _pool_kes_sk = subprocess.check_output(
            f'jcli key generate --type SumEd25519_12',
            shell=True,
            executable=self.executable
        ).decode()[:-1]

        os.system(f'echo {_pool_kes_sk} | jcli key to-public > p.tmp')

        with open('p.tmp', 'r') as f:
            _pool_kes_pk = f.read()[:-1]
        os.remove('p.tmp')

        #  3 Create New Stake Pool Registration Certificate
        os.system(f'jcli certificate new stake-pool-registration --kes-key {_pool_kes_pk} --vrf-key {_pool_vrf_pk} --owner {pk} --serial 1010101010 --start-validity 0 --management-threshold 1 >stake_pool.cert')

        with open('stake_pool.cert', 'r') as f:
            stake_pool_cert = f.read()[:-1]
        with open('stake_pool.cert', 'w') as f:
            f.write(stake_pool_cert)

        #  4 Sign the Stake Pool Registration Certificate With The Stake Pool Owner's Secret Key
        os.system(f'echo {sk} > stake_key.sk')
        #  os.system(f'cat stake_pool.cert | jcli certificate sign -k stake_key.sk > stake_pool.signcert')
        os.system(f'cat stake_pool.cert | jcli certificate get-stake-pool-id | tee stake_pool.id')

        fragment_id = self._send_certificate(account, sk)
        print('\nFragment ID: ', fragment_id[0])

        with open('stake_pool.id', 'r') as f:
            node_id = f.read()
            #  print('The Node ID is: ', f.read())



        command = f"""
cat > {pool_name}.yaml << EOF
genesis:
  sig_key: {_pool_kes_pk}
  vrf_key: {_pool_vrf_sk}
  node_id: {node_id}
EOF
"""
        os.system(command)

        if not os.path.exists('./pools'):
            os.makedirs('pools')

        os.rename(f'./{pool_name}.yaml', f'./pools/{pool_name}.yaml')
        os.remove('stake_pool.id')
        os.remove('stake_key.sk')

        return node_id

    def create_delegation_certificate(self, pool_id, pk, sk, account):
        with open('stake_pool.cert', 'w') as a:
            pass
        with open('stake_pool.signcert', 'w') as b:
            pass
        with open('key.tmp', 'w') as c:
            c.write(sk)

        os.system(f'jcli certificate new stake-delegation {pool_id} {pk} stake_pool.cert')
        #  os.system(f'jcli certificate sign key.tmp stake_pool.cert stake_pool.signcert')
        os.remove('key.tmp')

        with open('stake_pool.cert', 'r') as c, open('stake_pool.signcert', 'r') as s:
            cert_id = c.read()[:-1]
            signed_id = s.read()[:-1]
        with open('stake_pool.cert', 'w') as f:
            f.write(cert_id)

        #  print('Certificate: ', cert_id)
        #  print()
        #  print('Signed Certificate: ', signed_id)
        self._send_certificate(account, sk)
        return cert_id, signed_id

    def _send_certificate(self, sender, sk, counter=None):
        if counter is None:
            counter = self._get_counter(sender)

        try:
            coefficient, constant = self._get_coefficient_constant()
            cert = self._get_cert()

            with open('file.staging', 'w'):
                pass
            with open('stake_pool.cert', 'r') as r:
                certificate = r.read()

            #  Required transaction fees.
            total_fees = str(cert + coefficient + constant)
            print(f"\nCertificate Fee: {str(cert)} \nCoefficient: {str(coefficient)} \nFee Constant: {str(constant)} \nTotal: {str(total_fees)}")

            #  1 Create the Offline Staging File.
            os.system('jcli transaction new --staging file.staging')
            #  2 Add the Account to the Transaction
            os.system(f'jcli transaction add-account {sender} {total_fees} --staging file.staging')
            #  3 Add the Certificate to the Transaction
            os.system(f'jcli transaction add-certificate {certificate} --staging file.staging')
            #  4 Finalize the Transaction
            os.system('jcli transaction finalize --staging file.staging')
            witness = subprocess.check_output(
                'jcli transaction data-for-witness --staging file.staging',
                shell=True,
                executable=self.executable
            ).decode()[:-1]

            #  Create files for witness via python. JCLI requires environmental variables.
            with open('witness.output.tmp', 'w+') as f:
                pass
            with open('witness.secret.tmp', 'w+') as f:
                f.write(sk)

            #  5  Make the Witness.
            os.system(
                f'jcli transaction make-witness {witness} --genesis-block-hash {self.genesis} --type "account" --account-spending-counter {str(counter)} witness.output.tmp witness.secret.tmp'
            )

            #  6 Add the Witness to the Transaction.
            os.system(
                'jcli transaction add-witness witness.output.tmp --staging file.staging'
            )
            #  7 Show Transaction Info
            info = subprocess.check_output(
                f'jcli transaction info --fee-constant {str(constant)} --fee-coefficient {str(coefficient)} --fee-certificate {str(cert)} --staging file.staging',
                shell=True,
                executable=self.executable
            ).decode()

            #  8 Finalize the Transaction and Send to Blockchain
            os.system('jcli transaction seal --staging file.staging')
            os.system(f'jcli transaction auth -k stake_key.sk --staging file.staging')
            fragment_id = subprocess.check_output(
                f'jcli transaction to-message --staging file.staging | jcli rest v0 message post -h {self.node}/api',
                shell=True,
                executable=self.executable
            ).decode()

            #  Remove temp files, return tx not sent.
            self._remove_tmp()

            return fragment_id, total_fees, cert, coefficient, constant

        except IndexError:
            print('Unable to connect to node')
            print('Verify account is active and check node')
            self._remove_tmp()
            return False

#################### SEND TX #########################
    def _get_coefficient_constant(self):
        #  Extract the tx fee (coefficient and constant) from the node using string slicing.
        data = subprocess.check_output(
            f'jcli rest v0 settings get -h {self.node}/api',
            shell=True,
            executable=self.executable
        ).decode().replace(' ', '')

        data_dict = dict(s.split(':') for s in (data.split('\n')[7:9]))
        _coefficient = data_dict['coefficient']
        _constant = data_dict['constant']

        return int(_coefficient), int(_constant)

    def _get_counter(self, sender):
        try:
            #  Extract the required counter.
            os.system(
                f'jcli rest v0 account get {sender} -h {self.node}/api > balance.tmp')
            with open('balance.tmp', 'r') as f:
                counter = f.read().split()[2]
            os.remove('balance.tmp')

            return int(counter)

        except IndexError:
            print('Unable to connect to node, verify node is online.')

    def _send_tx(self, amount, sender, receiver, sk, counter = None):
        _force_send = False
        if counter is None:
            counter = self._get_counter(sender)
        else:
            _force_send = True

        try:
            coefficient, constant = self._get_coefficient_constant()

            #  Required transaction fees.
            total_fees = str(int(amount) + (coefficient * 2) + constant)
            #  print(coefficient, constant, total_fees)
            #  Begin tx procedure through JCLI.
            os.system('jcli transaction new --staging file.staging')
            os.system(f'jcli transaction add-account {sender} {total_fees} --staging file.staging')
            os.system(f'jcli transaction add-output  {receiver} {amount} --staging file.staging')
            os.system('jcli transaction finalize --staging file.staging')
            witness = subprocess.check_output(
                'jcli transaction data-for-witness --staging file.staging',
                shell=True,
                executable=self.executable
            ).decode()[:-1]

            #  Create files for witness via python. JCLI requires environmental variables.
            with open('witness.output.tmp', 'w+') as f:
                pass
            with open('witness.secret.tmp', 'w+') as f:
                f.write(sk)

            #  Include genesis block.
            os.system(
                f'jcli transaction make-witness {witness} --genesis-block-hash {self.genesis} --type "account" --account-spending-counter {str(counter)} witness.output.tmp witness.secret.tmp'
            )

            #  Add witness.
            os.system(
                'jcli transaction add-witness witness.output.tmp --staging file.staging'
            )
            info = subprocess.check_output(
                f'jcli transaction info --fee-constant {str(constant)} --fee-coefficient {str(coefficient)} --staging file.staging',
                shell=True,
                executable=self.executable
            ).decode()

            #  Display transaction info for sender to verify.
            #  print(info, "\n")
            #  Sender to confirm transaction.

            if _force_send is True:
                cont = 'y'
            else:
                cont = input('Commit transaction to blockchain? (y/n): ')

            if cont == 'y':
                #  Sender confirms, tx sends, return tx sent.
                os.system('jcli transaction seal --staging file.staging')
                #  os.system(
                #      f'jcli transaction to-message --staging file.staging | jcli rest v0 message post -h {self.node}/api'
                #  )
                fragment_id = subprocess.check_output(
                    f'jcli transaction to-message --staging file.staging | jcli rest v0 message post -h {self.node}/api',
                    shell=True,
                    executable=self.executable
                ).decode()

                fragment_id = fragment_id.replace(" ", "").replace("\n", "")
                #  print("FRAGMENTID: ", fragment_id)
                #  Remove temp files
                self._remove_tmp()

                return fragment_id, info
            else:
                #  Remove temp files, return tx not sent.
                self._remove_tmp()
                return False

        except IndexError:
            print('Unable to connect to node')
            print('Verify account is active and check node')
            self._remove_tmp()
            return False

        except ValueError:
            print('Unable to send, verify amount is an integer')
            self._remove_tmp()
            return False

    def send_multiple_tx(self, amount, sender, reciever, secret, rounds, await_each=True):
        nonce = self._get_counter(sender)
        _awaited_nonce = nonce + rounds
        for x in range(rounds):
            _new_nonce = int(nonce) + int(x)
            self._send_tx(
                amount,
                sender,
                reciever,
                secret,
                _new_nonce
            )
            if await_each is True:
                self._await_nonce(sender, _new_nonce)

        if await_each is False:
            self._await_nonce(sender, _awaited_nonce)
        return True

    def send_single_tx(self, amount, sender, reciever, secret, _nonce=None):
        nonce = self._get_counter(sender)
        _awaited_nonce = nonce + 1
        self._send_tx(
            amount,
            sender,
            reciever,
            secret,
            nonce
        )
        self._await_nonce(sender, _awaited_nonce)
        return True

    def _await_nonce(self, sender, _awaited_nonce):
        print(f"AWAITED NONCE: {_awaited_nonce}")
        confirmation = True
        while confirmation:
            _current_nonce = self._get_counter(sender)
            #  could happen, shouldnt
            if _current_nonce is None:
                self._await_nonce(sender, _awaited_nonce)

            if _current_nonce >= _awaited_nonce:
                _current_nonce = self._get_counter(sender)
                confirmation = False
                print(f"TRANSACTIONS CONFIRMED\nCurrent Nonce: {_current_nonce} / {_awaited_nonce}")
            else:
                _current_nonce = self._get_counter(sender)
                print(f"Current Nonce: {_current_nonce} / {_awaited_nonce}")
                time.sleep(5)

import pprint, json

import sys
sys.path.append(".")

from casper import CasperCore
from casper.utils import verify_password
USER_PWD = input("Enter your password\n")

if verify_password(USER_PWD) is False:
    print("PASSWORD IS NOT STRONG ENOUGH")

with open('settings.json', 'r') as json_file:
    settings = json.load(json_file)


casper = CasperCore(settings, USER_PWD)
#  imagine a button would trigger this function
def create_and_insert_acct():
    _sk, _pk, _ak = casper.cli.create_acct()
    casper.db.save_acct(_sk, _pk, _ak)
    myaccounts = casper.db.all_acct()
    print(myaccounts)

create_and_insert_acct()

print(casper.db.cipher.hash256("hashthisstring"))

print(casper.db._get_users())
acct = casper.db.get_acct_by_id(1)
reciever = casper.db.get_acct_by_id(5)
print(acct)

pprint.pprint(casper.node.show_stats())
pprint.pprint(casper.node.show_peers())

print(casper.node.show_stake())
pprint.pprint(casper.node.show_stake_pools())
pprint.pprint(casper.cli.show_balance(acct[1]))
print(casper.cli.message_logs())

print(casper.cli.prefix("wiz", acct[3]))

print(casper.cli._run('node --version'))

print(casper.cli._get_coefficient_constant())
nonce = casper.cli._get_counter(acct[1])
print(f"WALLET NONCE: {nonce}")

pprint.pprint(casper.node.show_node_stats())

casper.cli.send_single_tx(
    1,
    acct[1],
    reciever[1],
    acct[2]
)

casper.cli.send_multiple_tx(
    1,
    acct[1],
    reciever[1],
    acct[2],
    3,
    False
)

receivers = [
    "ca1s4ams4lc9zxsw50kfvh6wj3vzhpf4vt4n7vs0uavm6xuj4hh8lu9ulf73um",
    "ca1s5vf3arzrpwhtzutqua9539y4utpxqrwx2wd4t25drs0ya5agvfgkxn905m",
    "ca1s42xljdpqq7ryvl7m4d32u53dym0zxpvuv0ta0kcm80tf2e9ptnl2xwdsvc",
    "ca1sk6j2gqlulwwkd57639d0h3hp5j3xa6pue5rdyutsxlsg9yhrffhvdjdxew",
    "ca1shw30ett8fq5m37xty7dp3t6x2p2740av67hp3qrf0zmtd6z7sfsyv2sczu",
    "ca1shxy78kcd36p4hu0lwfggv4u66elpe2e3e50m0qfuchjgk6x70nkk5e59kp",
    "ca1skngaxqlr52syv26ssqsm2439mt4hkhamefq6rtrygkaz2vcmzc4vz4y2w6",
    "ca1sh79xe4dj4s3pkr9tlf40s6yhlnp3zj2rzeneczevljcetqy8lzczg92mfv",
    "ca1s4jm08fcefddxg9pj47fmtajejjm4nly5c5urhdj2mra4dn9535gxq47d8t",
    "ca1s53fav8th72cc03y88ynze88gfa92fljwredacr2w24yweduw6sp7l4gymy",
    "ca1shn9wwezwtfaxjclckmyq7kvj4qxqh8h4hn9yvrpdajr369j26ay29596qz",
    "ca1shu569z32t27raepsz73wrnc9jrh2kaulchtgdzsl5arvtwsc7fqxjrk8u7",
    "ca1shgdv9thhxf66pnqljsp886wpr0srt7dlrprrhz5lxdfxywyf8mqzfyppwm"
]

for addr in receivers:
    print(addr)
    casper.cli.send_single_tx(
        1000000,
        acct[1],
        addr,
        acct[2]
    )

INSERT INTO poolcerts (
  certificate, account_sk,
  vrf_secret, vrf_public,
  kes_secret, kes_public,
  pool_id, module,
  create_date, user_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

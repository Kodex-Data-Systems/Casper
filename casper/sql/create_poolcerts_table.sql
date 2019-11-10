CREATE TABLE IF NOT EXISTS 'poolcerts'
(
  'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'certificate' TEXT NOT NULL,
  'account_sk' TEXT NOT NULL,
  'vrf_secret' TEXT NOT NULL ,
  'vrf_public' TEXT NOT NULL,
  'kes_secret' TEXT NOT NULL ,
  'kes_public' TEXT NOT NULL,
  'pool_id' TEXT NOT NULL,
  'module' TEXT NOT NULL,
  'create_date' INTEGER,
  'user_id' INTEGER
)

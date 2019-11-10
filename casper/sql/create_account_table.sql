CREATE TABLE IF NOT EXISTS 'accounts'
(
  'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'account' TEXT NOT NULL,
  'secret' TEXT NOT NULL ,
  'public' TEXT NOT NULL,
  'module' TEXT NOT NULL,
  'create_date' INTEGER,
  'user_id' INTEGER
)

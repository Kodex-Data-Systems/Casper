CREATE TABLE IF NOT EXISTS 'fragments'
(
  'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'account' TEXT NOT NULL,
  'fragment_id' TEXT NOT NULL ,
  'value' TEXT NOT NULL,
  'create_date' INTEGER
)

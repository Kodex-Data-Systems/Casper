CREATE TABLE IF NOT EXISTS 'fragments'
(
  'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'fragment_id' TEXT NOT NULL ,
  'sender' TEXT NOT NULL,
  'receiver' TEXT NOT NULL,
  'value' TEXT NOT NULL,
  'create_date' INTEGER,
  'status' TEXT NOT NULL
)

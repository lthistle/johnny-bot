CREATE TABLE IF NOT EXISTS chickens (
    id integer PRIMARY KEY,
    user_id text NOT NULL UNIQUE,
    points integer,
    chicken_winrate integer
);

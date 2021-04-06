CREATE TABLE IF NOT EXISTS chickens (
    id integer PRIMARY KEY,
    user_id text NOT NULL UNIQUE,
    points integer,
    chicken_winrate integer,
    active_bet boolean
);

CREATE TABLE IF NOT EXISTS chicken_leaderboard (
    id integer PRIMARY KEY,
    user_id text NOT NULL UNIQUE,
    chicken_winrate integer,
    chicken_alive boolean
);

CREATE TABLE IF NOT EXISTS points_leaderboard (
    id integer PRIMARY KEY,
    user_id text NOT NULL UNIQUE,
    points integer
);
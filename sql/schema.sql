CREATE TABLE IF NOT EXISTS chickens (
    id integer PRIMARY KEY,
    user_id text NOT NULL UNIQUE,
    points integer,
    chicken_winrate integer,
    active_bet boolean
);

CREATE TABLE IF NOT EXISTS counter_table (
    guild_id integer NOT NULL UNIQUE,
    channel_id integer NOT NULL UNIQUE,
    current_number integer,

    -- Server-wide stats
    highest_number integer,
    highest_number_timestamp integer,
    last_count integer,
    last_count_timestamp integer,
    longest_counting_delay_sec integer,
    last_counter_user_id integer
);

CREATE TABLE IF NOT EXISTS counter_leaderboard (
    user_id integer NOT NULL UNIQUE,
    highest_number integer,
    highest_number_timestamp integer,
    successful_counts integer,
    failed_counts integer,
    worst_miscount_num integer,
    worst_miscount_timestamp integer
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
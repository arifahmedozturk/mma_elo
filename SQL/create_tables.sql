CREATE TABLE fighters(
    fighter_name TEXT PRIMARY KEY,
    elo INT,
    dob TEXT,
    last_age_penalty TEXT
);

CREATE TABLE fights(
    id SERIAL PRIMARY KEY,
    fighter TEXT,
    opponent TEXT,
    result TEXT,
    date TEXT,
    method TEXT,
    event TEXT
);

CREATE TABLE elo_changes(
    id SERIAL PRIMARY KEY,
    fighter TEXT,
    opponent TEXT,
    opponent_elo INT,
    date TEXT,
    elo INT,
    new_elo INT
);

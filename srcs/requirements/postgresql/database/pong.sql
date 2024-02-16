-- Create the users table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    intra_name VARCHAR(50) UNIQUE,
    name VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    normal_games_played INTEGER,
    normal_games_won INTEGER,
    normal_win_streak INTEGER,
    tournaments_won INTEGER,
    date_of_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assign ownership of the users table to the database owner
ALTER TABLE IF EXISTS users OWNER TO pong;

-- Create the tournaments table if it does not exist
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_id SERIAL PRIMARY KEY,
    tournament_name VARCHAR(100),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    winner_id INTEGER REFERENCES users(user_id),
    game_ids INTEGER[]
);

-- Assign ownership of the tournaments table to the database owner
ALTER TABLE IF EXISTS tournaments OWNER TO pong;

-- Create the games table if it does not exist
CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(tournament_id),
    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    winner_id INTEGER REFERENCES users(user_id),
    participants INTEGER[],
    is_tournament BOOLEAN DEFAULT FALSE
);

-- Assign ownership of the games table to the database owner
ALTER TABLE IF EXISTS games OWNER TO pong;
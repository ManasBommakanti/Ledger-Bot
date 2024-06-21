CREATE TABLE IF NOT EXISTS Ledger (
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserFrom TEXT NOT NULL,
    UserTo TEXT NOT NULL,
    Amount INTEGER NOT NULL,
    TransactionTime FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS Leaderboard (
    UserID TEXT NOT NULL PRIMARY KEY,
    Amount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS RunningStats (
    RunningID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT NOT NULL,
    RunningAmount INTEGER NOT NULL,
    Time FLOAT NOT NULL
);
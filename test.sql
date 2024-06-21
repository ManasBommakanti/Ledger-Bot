-- Used to update RunningStats table
CREATE TABLE Temp (
    RunningID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT NOT NULL,
    RunningAmount INTEGER NOT NULL,
    TransactionTime FLOAT NOT NULL
);

-- Initially, gather all transactions for each user and record as 
-- withdrawing (-) or depositing (+) transaction
INSERT INTO Temp (UserID, RunningAmount, TransactionTime)
SELECT
    UserFrom AS UserID,
    -Amount AS Amount,
    TransactionTime
FROM Ledger
UNION ALL
SELECT
    UserTo AS UserID,
    Amount AS Amount,
    TransactionTime
FROM Ledger;

-- Calculate the running sum at each transaction time
INSERT INTO RunningStats (UserID, RunningAmount, Time)
SELECT
    UserID,
    SUM(RunningAmount) OVER (PARTITION BY UserID ORDER BY TransactionTime) AS RunningAmount,
    TransactionTime
FROM Temp;

-- Drop Temp table as we do not need it anymore
DROP TABLE Temp;

-- Use RunningStats table to get the leaderboard
INSERT INTO Leaderboard
SELECT UserID, RunningAmount
FROM RunningStats
GROUP BY UserID
HAVING Time = MAX(Time)
ORDER BY RunningAmount DESC;
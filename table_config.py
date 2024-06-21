import sqlite3
import json
import asyncio
import os

lock = asyncio.Lock()

with open("config.json") as c:
    config = json.load(c)

CASINO_DB_FILEPATH = config["DATABASE"]["CASINO_DB_REL_PATH"]


def create_tables():
    conn = sqlite3.connect(CASINO_DB_FILEPATH)
    c = conn.cursor()

    with open(config["DATABASE"]["SCHEMA_REL_PATH"], "r") as f:
        c.executescript(f.read())

    conn.commit()

    c.close()
    conn.close()


def update_ledger_table_from_backup():
    conn = sqlite3.connect(CASINO_DB_FILEPATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(TransactionID) FROM Ledger;")
    num_rows = c.fetchone()
    print(num_rows)

    if num_rows[0] >= 0:
        c.execute("DELETE FROM Ledger;")

    with open(config["BACKUP_LEDGER"]) as b:
        backup_ledger = json.load(b)

    for row in backup_ledger:
        print(row)
        user_from = row["u_from"]
        user_to = row["u_to"]
        amount = row["amount"]
        transaction_time = row["t"]

        c.execute(
            """
            INSERT INTO Ledger (UserFrom, UserTo, Amount, TransactionTime)
            VALUES (?, ?, ?, ?);
            """,
            (user_from, user_to, amount, transaction_time),
        )

    conn.commit()

    c.close()
    conn.close()


def update_running_stats_and_leaderboard():
    conn = sqlite3.connect(CASINO_DB_FILEPATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(RunningID) FROM RunningStats;")
    num_rows = c.fetchone()
    print(num_rows)

    if num_rows[0] >= 0:
        c.execute("DELETE FROM RunningStats;")
        c.execute("DELETE FROM Leaderboard;")

    with open(config["DATABASE"]["UPDATE_TABLES"], "r") as f:
        c.executescript(f.read())

    conn.commit()

    c.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
    update_ledger_table_from_backup()
    update_running_stats_and_leaderboard()

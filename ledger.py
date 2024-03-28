import asyncio
from typing import TypedDict
import json

from time import time


class LedgerEntry(TypedDict):
    u_from: str
    u_to: str
    amount: int
    t: float


class PersistentLedger:
    def __init__(self, fname: str):
        self.fname = fname
        self.lock = asyncio.Lock()

        self.data: list[LedgerEntry] = self.load()
        self.save()

    def load(self):
        out = []
        pot_entry = {"u_from": "pot", "u_to": "pot", "amount": 0, "t": time()}
        out.append(pot_entry)

        try:
            with open(self.fname, "r") as f:
                out = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)
            pass

        return out

    def save(self):
        with open(self.fname, "w") as f:
            json.dump(self.data, f, indent=4)

    async def player_balance(self, ident: str):
        async with self.lock:
            neg = sum(e["amount"] for e in self.data if e["u_from"] == ident)
            pos = sum(e["amount"] for e in self.data if e["u_to"] == ident)

        return pos - neg

    async def unique_players(self):
        async with self.lock:
            players = set()
            for entry in self.data:
                players.add(entry["u_from"])
                players.add(entry["u_to"])

        return players

    def append(self, entry: LedgerEntry):
        self.data.append(entry)
        self.save()

from dataclasses import dataclass
from typing import List
import time


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    active: bool = True
    created_ts: float = time.time()

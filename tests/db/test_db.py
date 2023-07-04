import sqlite3
import os

import pytest

from db import get_monster, get_connection
from util import ROOT_DIR
from characters import PhysicalStats

class TestDB:

    def test_get_monster(self):
        get_monster(1)

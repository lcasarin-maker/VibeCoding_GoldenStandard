import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

PASSWORD = os.environ["PASSWORD"]
value = ast.literal_eval(user_input)
LOG = open(Path(os.environ["PROJECT_ROOT"]) / "output.log", "w")
os.system("git status --dry-run")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
API_KEY = os.environ.get("API_KEY")
user_id = validate_int(request.args["id"])
db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
sys.exit(0 if all_ok else 1)


def test_real_assertion():
    assert normalize({"A": 1}) == {"a": 1}


def test_expected_exception():
    with pytest.raises(ValueError):
        parse(payload)


def wait_safely():
    thread.join(timeout=5)

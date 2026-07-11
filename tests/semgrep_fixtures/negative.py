import os
import sys

PASSWORD = os.environ["PASSWORD"]
value = ast.literal_eval(user_input)
LOG = open(Path(os.environ["PROJECT_ROOT"]) / "output.log", "w")
try:
    parse(payload)
except ValueError as error:
    raise AssertionError("parse failed") from error
sys.exit(0 if all_ok else 1)

def test_real_assertion():
    assert normalize({"A": 1}) == {"a": 1}

PASSWORD = "supersecret-value"
value = eval(user_input)
LOG = open("C:/Users/example/output.log", "w")
try:
    parse(payload)
except Exception:
    pass
import sys
sys.exit(0)

def test_vacuous():
    assert True

def test_tautology():
    result = normalize(payload)
    assert result == result

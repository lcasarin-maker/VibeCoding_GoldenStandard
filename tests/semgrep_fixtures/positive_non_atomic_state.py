import json

with open("state.json", "w") as stream:
    json.dump(state, stream)

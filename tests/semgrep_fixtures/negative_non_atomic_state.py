import json
import os
import tempfile

descriptor, temporary = tempfile.mkstemp(dir=".")
with os.fdopen(descriptor, "w") as stream:
    json.dump(state, stream)
os.replace(temporary, "state.json")

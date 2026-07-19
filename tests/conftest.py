import os
import sys

# Ensure ~/.local/bin is in PATH for semgrep and other pip-installed tools
local_bin = os.path.expanduser("~/.local/bin")
if local_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{local_bin}:{os.environ.get("PATH", "")}"

import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)

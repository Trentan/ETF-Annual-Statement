import glob
import subprocess

for file in glob.glob(r"tax\v*.pdf"):
    subprocess.run(["etf2cb", file, "vanguard"], check=True)

for file in glob.glob(r"tax\beta*.pdf"):
    subprocess.run(["etf2cb", file, "Beta"], check=True)

import glob
import subprocess
import sys
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
python_exe = sys.executable  # uses same interpreter IntelliJ runs

for file in glob.glob(r"tax\statements\vanguard*.pdf"):
    print(f"Processing {file}...")
    try:
        subprocess.run(
            [python_exe, os.path.join(base_dir, "etf2cb.py"), file, "vanguard"],
            check=True,
            cwd=base_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on {file}: {e}")

for file in glob.glob(r"tax\statements\beta*.pdf"):
    print(f"Processing {file}...")
    try:
        subprocess.run(
            [python_exe, os.path.join(base_dir, "etf2cb.py"), file, "beta"],
            check=True,
            cwd=base_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on {file}: {e}")

for file in glob.glob(r"tax\statements\globalx*.pdf"):
    print(f"Processing {file}...")
    try:
        subprocess.run(
            [python_exe, os.path.join(base_dir, "etf2cb.py"), file, "globalx"],
            check=True,
            cwd=base_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on {file}: {e}")

for file in glob.glob(r"tax\statements\vaneck*.pdf"):
    print(f"Processing {file}...")
    try:
        subprocess.run(
            [python_exe, os.path.join(base_dir, "etf2cb.py"), file, "vaneck"],
            check=True,
            cwd=base_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on {file}: {e}")

for file in glob.glob(r"tax\statements\ishares*.pdf"):
    print(f"Processing {file}...")
    try:
        subprocess.run(
            [python_exe, os.path.join(base_dir, "etf2cb.py"), file, "ishares"],
            check=True,
            cwd=base_dir
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed on {file}: {e}")
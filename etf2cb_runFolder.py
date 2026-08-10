import glob
import os
import etf2cb

providers = [
    (r"tax\statements\vanguard*.pdf", "vanguard"),
    (r"tax\statements\beta*.pdf", "beta"),
    (r"tax\statements\globalx*.pdf", "globalx"),
    (r"tax\statements\vaneck*.pdf", "vaneck"),
    (r"tax\statements\ishares*.pdf", "ishares"),
]

for pattern, area in providers:
    for file in glob.glob(pattern):
        print(f"Processing {file}...", flush=True)
        try:
            etf2cb.process_statement(file, area)
        except Exception as e:
            print(f"[FAILED] on {file}: {e}", flush=True)
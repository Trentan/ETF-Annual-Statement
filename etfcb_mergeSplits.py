import os
import glob
import csv
from collections import defaultdict

input_folder = r"Tax\Statements"
output_file = r"Tax\combined_split_statements.csv"

csv_files = sorted(glob.glob(os.path.join(input_folder, "*split.csv")))

if not csv_files:
    print("[WARNING] No matching CSV files found.")
else:
    print(f"Combining {len(csv_files)} split CSV files...\n")

    # Store transactions: key = (Entity, Date, Description), value = dict of account -> amount_in_cents
    txns = defaultdict(lambda: defaultdict(int))
    txn_order = []

    for file in csv_files:
        print(f"-> Processing {os.path.basename(file)}")
        with open(file, "r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            for row in reader:
                if not row or len(row) < 5:
                    continue
                # Skip header if file happens to contain one
                if row[0].strip().lower() == "entity":
                    continue

                entity = row[0].strip()
                date = row[1].strip()
                desc = row[2].strip()
                account = row[3].strip()
                try:
                    deposit_cents = int(round(float(row[4].strip()) * 100))
                except ValueError:
                    continue

                key = (entity, date, desc)
                if key not in txns:
                    txn_order.append(key)
                
                txns[key][account] += deposit_cents

    print(f"\nConsolidated into {len(txn_order)} transactions.")

    with open(output_file, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        # Write GnuCash CSV Header
        writer.writerow(["Entity", "Date", "Description", "Account", "Deposit"])

        total_splits = 0
        for key in txn_order:
            entity, date, desc = key
            acc_map = txns[key]

            # Verify balance
            balance_cents = sum(acc_map.values())
            if balance_cents != 0:
                print(f"  [WARNING] Balance imbalance for {desc} ({entity}, {date}): {balance_cents/100:.2f}. Adjusting rounding split.")
                rounding_acc = "Income:Distribution:Rounding"
                acc_map[rounding_acc] -= balance_cents

            for account, cents in acc_map.items():
                deposit_str = f"{cents / 100:.2f}"
                writer.writerow([entity, date, desc, account, deposit_str])
                total_splits += 1

    print(f"Balance verification complete for all transactions.")
    print(f"Combined {total_splits} splits saved to: {output_file}\n")

import os
import glob

input_folder = r"Tax\Statements"
output_file = r"Tax\combined_split_statements.csv"

csv_files = glob.glob(os.path.join(input_folder, "*split.csv"))

if not csv_files:
    print("⚠️ No matching CSV files found.")
else:
    print(f"📂 Combining {len(csv_files)} split CSV files...\n")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for file in csv_files:
            print(f"→ Adding {os.path.basename(file)}")
            with open(file, "r", encoding="utf-8") as infile:
                for line in infile:
                    line = line.strip()
                    if not line:
                        continue  # skip blanks
                    # Add the filename as a new last column
                    outfile.write(f"{line}\n")

    print(f"\n✅ Combined file saved to: {output_file}")
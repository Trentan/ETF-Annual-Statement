import glob
import pandas as pd
import os

# Output file (note the uppercase 'Tax')
output_dir = "Tax"
output_file = os.path.join(output_dir, "all_splits.csv")

# Ensure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Find all matching split CSVs in the Tax folder
csv_files = glob.glob(os.path.join(output_dir, "*split.csv"))
print("Current working directory:", os.getcwd())
print("Found CSV files:", csv_files)

if not csv_files:
    print("⚠️ No split CSV files found — check your folder path or file names.")
else:
    csv_files.sort()
    combined = []

    for i, file in enumerate(csv_files):
        print(f"Processing: {file}")
        df = pd.read_csv(file)

        # Skip header rows except for first file
        if i == 0:
            combined.append(df)
        else:
            if "Entity" in df.columns[0]:
                combined.append(df.iloc[1:])
            else:
                combined.append(df)

    merged_df = pd.concat(combined, ignore_index=True)
    merged_df.to_csv(output_file, index=False)

    print(f"✅ Merged {len(csv_files)} files into {output_file}")

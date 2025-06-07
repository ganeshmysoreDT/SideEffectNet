import pandas as pd

# === Load raw data ===

# 1. Load all side effects (meddra_all_se)
se_df = pd.read_csv('data/raw/meddra_all_se.tsv', sep='\t', header=None,
                    names=['stitch_flat', 'stitch_stereo', 'umls_id', 'type', 'umls_id_dup', 'side_effect'])

# Drop duplicate UMLS column
se_df.drop(columns=['umls_id_dup'], inplace=True)

# 2. Load frequency data (meddra_freq)
freq_df = pd.read_csv('data/raw/meddra_freq.tsv', sep='\t', header=None,
                      names=[
                          'stitch_flat', 'stitch_stereo', 'umls_id', 'placebo_freq',
                          'freq_str', 'freq_float', 'freq_adjusted',
                          'type', 'umls_id_dup', 'side_effect'
                      ])

# Keep only stitch_flat, umls_id, freq_float
freq_df = freq_df[['stitch_flat', 'umls_id', 'freq_float']]

# 3. Load drug names
names_df = pd.read_csv('data/raw/drug_names.tsv', sep='\t', header=None, names=['stitch_id', 'drug_name'])

# === Merge data ===

# Merge se_df with drug names
merged_df = se_df.merge(names_df, left_on='stitch_flat', right_on='stitch_id', how='left')

# Merge with frequency info
merged_df = merged_df.merge(freq_df, on=['stitch_flat', 'umls_id'], how='left')

# Rename columns for clarity
merged_df.rename(columns={
    'stitch_flat': 'stitch_id',
    'freq_float': 'freq_pct'
}, inplace=True)

# Reorder and select final columns
final_df = merged_df[['stitch_id', 'drug_name', 'umls_id', 'side_effect', 'type', 'freq_pct']]

# Save cleaned data
final_df.to_csv('data/processed/side_effects_clean.csv', index=False, sep=',', encoding='utf-8')

print("Cleaned data saved to data/processed/side_effects_clean.csv")

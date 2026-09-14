# ============================================================
# Kitwe City Council Data — Full Cleaning & Merging Pipeline
# ============================================================
# This script combines ALL steps used to clean, merge, and
# deduplicate the two source CSV files into a combined dataset
# and a separate duplicates/overlaps file.
#
# Source files:
#   1. kitwe_city_council_data__1_(1).csv  (File 1 — 157 rows, 18 cols)
#      Manually extracted from audited financial statements &
#      budget performance reports
#   2. DataMining-project.csv               (File 2 — 807 rows, 9 cols)
#      Data-mined from council minutes, CDF project lists,
#      and budget estimate PDFs
#
# Outputs:
#   - kitwe_city_council_combined.csv      (963 rows × 12 cols)
#   - kitwe_city_council_data__1_(1).csv    (120 rows × 12 cols)
# ============================================================

import pandas as pd
import numpy as np
import re

# ============================================================
# PART 1: LOAD ORIGINAL FILES
# ============================================================

f1_orig = pd.read_csv('uploads/kitwe_city_council_data__1_(1).csv', dtype=str)
f2_orig = pd.read_csv('uploads/DataMining-project.csv', dtype=str)

print(f'File 1 original: {f1_orig.shape[0]} rows, {f1_orig.shape[1]} columns')
print(f'File 2 original: {f2_orig.shape[0]} rows, {f2_orig.shape[1]} columns')
print()

# ============================================================
# PART 2: CLEAN FILE 1 — Fix column misalignment
# ============================================================
# File 1 has many rows where a "description" field exists between
# actual_zmw and source_document, but the CSV header doesn't
# include it. This causes source_document → scope to shift right
# by one column. We detect this by checking whether the
# source_document column actually contains a filename.

filename_pattern = re.compile(r'\.(pdf|docx|xlsx|doc|csv)$', re.IGNORECASE)
filename_keywords = [
    'Budget-Performance', 'KCC', 'Kitwe-City-Council',
    'Kitwe-C-C', 'Kitwe Financial', 'SUMMARY-OF-ACTION'
]

def is_filename(val):
    """Check if a value looks like a source document filename."""
    if pd.isna(val) or str(val).strip() == '':
        return False
    val = str(val).strip()
    if filename_pattern.search(val):
        return True
    for kw in filename_keywords:
        if kw in val:
            return True
    return False

# Identify rows where source_document does NOT contain a filename
# These are the "shifted" rows that need realignment
shifted = ~f1_orig['source_document'].apply(is_filename)
print(f'File 1 shifted rows: {shifted.sum()}')
print(f'File 1 properly aligned rows: {(~shifted).sum()}')

# For shifted rows, the real mapping is:
#   current source_document → description (the hidden field)
#   current source_table    → source_document (the real filename)
#   current source_page     → source_table
#   current scope           → source_page
#   scope should be cleared (the real scope was lost)
new_description = pd.Series(np.nan, index=f1_orig.index, dtype=object)
new_source_document = f1_orig['source_document'].copy()
new_source_table = f1_orig['source_table'].copy()
new_source_page = f1_orig['source_page'].copy()
new_scope = f1_orig['scope'].copy()

# Pull values left by one position for shifted rows
new_description[shifted] = f1_orig.loc[shifted, 'source_document'].values
new_source_document[shifted] = f1_orig.loc[shifted, 'source_table'].values
new_source_table[shifted] = f1_orig.loc[shifted, 'source_page'].values
new_source_page[shifted] = f1_orig.loc[shifted, 'scope'].values
new_scope[shifted] = np.nan

# Insert the new 'description' column after actual_zmw (position 10)
cols = list(f1_orig.columns)
cols.insert(10, 'description')
f1_orig = f1_orig.reindex(columns=cols)

# Apply the corrected values
f1_orig['description'] = new_description.values
f1_orig['source_document'] = new_source_document.values
f1_orig['source_table'] = new_source_table.values
f1_orig['source_page'] = new_source_page.values
f1_orig['scope'] = new_scope.values

# ============================================================
# PART 3: CLEAN FILE 1 — Remove empty duplicate row
# ============================================================
# Record KIT-EXP-2023-004 has an ID but all financial values
# (budget_zmw, actual_zmw) are NaN — effectively a blank row.

print(f"\nRemoving KIT-EXP-2023-004 (empty duplicate): {len(f1_orig[f1_orig['record_id'] == 'KIT-EXP-2023-004'])} row(s)")
f1_orig = f1_orig[f1_orig['record_id'] != 'KIT-EXP-2023-004'].copy().reset_index(drop=True)
print(f'File 1 after removing empty row: {f1_orig.shape[0]} rows')

# ============================================================
# PART 4: CLEAN FILE 1 — Fill missing line_item from category
# ============================================================
# Some expenditure rows have a category but no line_item.
# We copy the category value into line_item so every row has one.

missing_line = f1_orig['line_item'].isna() | (f1_orig['line_item'].str.strip() == '')
print(f'\nFile 1 rows with missing line_item: {missing_line.sum()}')
f1_orig.loc[missing_line, 'line_item'] = f1_orig.loc[missing_line, 'category']

# ============================================================
# PART 5: CLEAN FILE 1 — Fix specific misaligned rows
# ============================================================
# One row (source_document = "27") had its source_document replaced
# by a page number. The real source doc is
# Budget-Performance-Report-116-LAs.pdf.

bad_row = f1_orig[f1_orig['source_document'] == '27']
if len(bad_row) > 0:
    idx = bad_row.index[0]
    f1_orig.at[idx, 'description'] = f1_orig.at[idx, 'source_table']
    f1_orig.at[idx, 'source_document'] = 'Budget-Performance-Report-116-LAs.pdf'
    f1_orig.at[idx, 'source_table'] = 'Table 14'
    f1_orig.at[idx, 'source_page'] = '27'
    f1_orig.at[idx, 'scope'] = 'Province-wide'
    print(f'Fixed misaligned row {idx}: source_document set to Budget-Performance-Report-116-LAs.pdf')

# Another row had source_page = "10/09/2026" — a date leaked in
bad_date = f1_orig[f1_orig['source_page'] == '10/09/2026']
if len(bad_date) > 0:
    idx = bad_date.index[0]
    f1_orig.at[idx, 'source_page'] = '27'
    f1_orig.at[idx, 'description'] = str(f1_orig.at[idx, 'description']) + ' (as of 10/09/2026)'
    print(f'Fixed date leak in source_page row {idx}')

# ============================================================
# PART 6: CLEAN FILE 1 — Convert numeric columns
# ============================================================

f1_orig['budget_zmw'] = pd.to_numeric(f1_orig['budget_zmw'], errors='coerce')
f1_orig['actual_zmw'] = pd.to_numeric(f1_orig['actual_zmw'], errors='coerce')
f1_orig['fiscal_year'] = pd.to_numeric(f1_orig['fiscal_year'], errors='coerce').astype('Int64')

# Strip whitespace from text columns
text_cols = ['record_type', 'category', 'line_item', 'council_name',
             'province', 'period', 'source_document', 'source_table', 'currency']
for col in text_cols:
    if col in f1_orig.columns:
        f1_orig[col] = f1_orig[col].str.strip()

f1_clean = f1_orig.copy()
print(f'\nFile 1 cleaned shape: {f1_clean.shape}')

# ============================================================
# PART 7: CLEAN FILE 2 — Classify row types
# ============================================================
# File 2 has three distinct data types mixed together:
#   a) council_minutes — from .docx minutes files
#   b) cdf_project — from CDF project PDFs
#   c) budget_line_item — from budget estimate PDFs
# Each type has different column meanings (see Part 8).

def classify_row(source_doc):
    s = str(source_doc).strip().upper()
    if any(kw in s for kw in ['COUNCIL-MINUTES', '3RD-OCTOBER',
                              '30TH-JUNE', 'DISABILITIES', 'STAKEHOLDERS']):
        return 'council_minutes'
    elif 'CDF' in s:
        return 'cdf_project'
    else:
        return 'budget_line_item'

f2_orig['row_type'] = f2_orig['Source Document'].apply(classify_row)
print(f'\nFile 2 row types: {f2_orig["row_type"].value_counts().to_dict()}')

# ============================================================
# PART 8: CLEAN FILE 2 — Fix column misalignment
# ============================================================
# File 2's columns are misused depending on the row type:
#
# For budget_line_item rows:
#   "Seconder" column actually holds the budget AMOUNT (numeric)
#   "Amount (K)" column holds the BUDGET YEAR LABEL
#     (e.g. "2026 Approved Budget")
#   The real Seconder/Proposer values are missing.
#
# For cdf_project rows:
#   "Seconder" column holds the FUNDING SOURCE
#     (e.g. "2024 CDF funding")
#   "Amount (K)" is empty or holds leaked text
#
# For council_minutes rows:
#   Columns are correctly aligned

budget_mask = f2_orig['row_type'] == 'budget_line_item'
cdf_mask = f2_orig['row_type'] == 'cdf_project'

# --- Budget rows: extract budget year label and real amount ---
f2_orig.loc[budget_mask, '_budget_year_label'] = f2_orig.loc[budget_mask, 'Amount (K)']
f2_orig.loc[budget_mask, '_amount_zmw'] = f2_orig.loc[budget_mask, 'Seconder']

# Clear the misaligned columns
f2_orig.loc[budget_mask, 'Seconder'] = np.nan
f2_orig.loc[budget_mask, 'Proposer'] = np.nan
f2_orig.loc[budget_mask, 'Amount (K)'] = np.nan

# --- CDF rows: extract funding source from Seconder ---
f2_orig.loc[cdf_mask, '_funding_source'] = f2_orig.loc[cdf_mask, 'Seconder']
f2_orig.loc[cdf_mask, '_budget_year_label'] = np.nan
f2_orig.loc[cdf_mask, '_amount_zmw'] = np.nan
f2_orig.loc[cdf_mask, 'Seconder'] = np.nan

# --- Council minutes rows: already correct ---
f2_orig.loc[~budget_mask & ~cdf_mask, '_budget_year_label'] = np.nan
f2_orig.loc[~budget_mask & ~cdf_mask, '_amount_zmw'] = np.nan
f2_orig.loc[~budget_mask & ~cdf_mask, '_funding_source'] = np.nan

# ============================================================
# PART 9: CLEAN FILE 2 — Fix leaked data in Notes/Amount columns
# ============================================================
# Some rows had the source document filename leaked into the Notes column.
# One row had source document text leaked into Amount (K).

# Fix stakeholders meeting rows where source doc leaked into Notes
for i, row in f2_orig.iterrows():
    if row['row_type'] == 'council_minutes' and str(row['Notes']).startswith('STAKEHOLDERS'):
        f2_orig.at[i, 'Source Document'] = 'STAKEHOLDERS-MEETING-MINUTUES-PERSON-WITH-DISABILITIES.pdf'
        f2_orig.at[i, 'Notes'] = np.nan

# Standardize the disabilities filename
f2_orig['Source Document'] = f2_orig['Source Document'].replace({
    'DISABILITIES.pdf': 'STAKEHOLDERS-MEETING-MINUTUES-PERSON-WITH-DISABILITIES.pdf'
})

# Fix row where Amount (K) contained leaked source doc text
leaked_rows = f2_orig[f2_orig['Amount (K)'].str.contains('2026-budget', na=False)]
for i in leaked_rows.index:
    val = str(f2_orig.at[i, 'Amount (K)'])
    match = re.match(r'^(\d{4}\s+\w+\s+Budget)', val)
    if match:
        f2_orig.at[i, 'Amount (K)'] = match.group(1)
        print(f'Fixed leaked source doc in Amount (K) at row {i}: kept "{match.group(1)}"')

# ============================================================
# PART 10: CLEAN FILE 2 — Extract fiscal year
# ============================================================
# Fiscal year comes from different places depending on row type:
#   budget rows → extracted from _budget_year_label
#   CDF rows    → extracted from _funding_source (e.g. "2024 CDF")
#   minutes     → extracted from Source Document filename

def extract_fiscal_year(label):
    """Pull the 4-digit year from a budget year label string."""
    if pd.isna(label) or str(label).strip() in ('', 'nan'):
        return np.nan
    match = re.match(r'(\d{4})', str(label))
    return match.group(1) if match else np.nan

# Budget rows
f2_orig['fiscal_year'] = f2_orig['_budget_year_label'].apply(extract_fiscal_year)

# CDF rows — override with year from funding source
def extract_cdf_fy(row):
    if row['row_type'] != 'cdf_project':
        return row.get('fiscal_year', np.nan)
    fs = str(row.get('_funding_source', ''))
    match = re.search(r'(\d{4})', fs)
    return match.group(1) if match else np.nan

f2_orig['fiscal_year'] = f2_orig.apply(extract_cdf_fy, axis=1)

# Council minutes — extract from source document filename
min_mask = f2_orig['row_type'] == 'council_minutes'
def extract_minutes_fy(row):
    if row['row_type'] != 'council_minutes':
        return row.get('fiscal_year', np.nan) if pd.notna(row.get('fiscal_year')) else np.nan
    src = str(row['Source Document'])
    match = re.search(r'(\d{4})', src)
    return match.group(1) if match else np.nan

f2_orig.loc[min_mask, 'fiscal_year'] = f2_orig[min_mask].apply(extract_minutes_fy, axis=1)

# ============================================================
# PART 11: CLEAN FILE 2 — Map record types
# ============================================================
# Convert File 2's "Category / Type" values into our unified
# record_type vocabulary:
#   Resolution → council_resolution
#   Motion      → council_motion
#   Submission/Discussion/Recommendation/Closing → council_proceeding
#   Revenue     → budget_revenue
#   Expenditure → budget_expenditure
#   Proposed    → cdf_proposed_project
#   Approved     → cdf_approved_project

def map_record_type(row):
    rt = row['row_type']
    cat = str(row['Category / Type']).strip()
    if rt == 'council_minutes':
        if cat == 'Resolution':
            return 'council_resolution'
        elif cat == 'Motion':
            return 'council_motion'
        elif cat in ('Submission', 'Discussion', 'Recommendation', 'Closing'):
            return 'council_proceeding'
        else:
            return 'council_proceeding'
    elif rt == 'budget_line_item':
        if cat == 'Revenue':
            return 'budget_revenue'
        elif cat == 'Expenditure':
            return 'budget_expenditure'
        else:
            return 'budget_line_item'
    elif rt == 'cdf_project':
        if cat == 'Proposed':
            return 'cdf_proposed_project'
        elif cat == 'Approved':
            return 'cdf_approved_project'
        else:
            return 'cdf_project'
    return 'unknown'

f2_orig['record_type'] = f2_orig.apply(map_record_type, axis=1)
print(f'\nFile 2 record types: {f2_orig["record_type"].value_counts().to_dict()}')
print(f'File 2 fiscal years: {f2_orig["fiscal_year"].value_counts().to_dict()}')

# ============================================================
# PART 12: CREATE UNIFIED COLUMN SCHEMA
# ============================================================
# Map both files to a common superset of 26 columns.
# File 2 has some columns File 1 doesn't (and vice versa),
# so we create empty placeholders where needed.

unified_cols = [
    'record_id', 'record_type', 'council_name', 'province', 'fiscal_year',
    'period', 'category', 'line_item', 'budget_zmw', 'actual_zmw',
    'description', 'source_document', 'source_table', 'source_page',
    'scope', 'currency', 'ward_or_constituency', 'stakeholders',
    'reference_code', 'key_resolution', 'proposer', 'seconder',
    'amount_zmw', 'budget_year_label', 'funding_source', 'notes'
]

# ============================================================
# PART 13: MAP FILE 1 TO UNIFIED SCHEMA
# ============================================================

f1_mapped = pd.DataFrame()
f1_mapped['record_id']      = f1_clean['record_id']
f1_mapped['record_type']    = f1_clean['record_type']
f1_mapped['council_name']   = f1_clean['council_name']
f1_mapped['province']      = f1_clean['province']
f1_mapped['fiscal_year']    = f1_clean['fiscal_year']
f1_mapped['period']        = f1_clean['period']
f1_mapped['category']      = f1_clean['category']
f1_mapped['line_item']     = f1_clean['line_item']
f1_mapped['budget_zmw']    = f1_clean['budget_zmw']
f1_mapped['actual_zmw']    = f1_clean['actual_zmw']
f1_mapped['description']   = f1_clean['description']
f1_mapped['source_document'] = f1_clean['source_document']
f1_mapped['source_table']  = f1_clean['source_table']
f1_mapped['source_page']   = f1_clean['source_page']
f1_mapped['scope']         = f1_clean['scope']
f1_mapped['currency']      = f1_clean['currency']
f1_mapped['ward_or_constituency'] = f1_clean['ward_or_constituency']
f1_mapped['stakeholders']  = f1_clean['stakeholders']

# File 1 doesn't have these columns — leave empty
for col in ['reference_code', 'key_resolution', 'proposer', 'seconder',
             'amount_zmw', 'budget_year_label', 'funding_source', 'notes']:
    f1_mapped[col] = np.nan

f1_mapped = f1_mapped[unified_cols]

# ============================================================
# PART 14: MAP FILE 2 TO UNIFIED SCHEMA
# ============================================================

f2_mapped = pd.DataFrame()
f2_mapped['record_id']      = np.nan  # Will be generated below
f2_mapped['record_type']   = f2_orig['record_type']
f2_mapped['council_name']  = 'Kitwe City Council'
f2_mapped['province']      = 'Copperbelt'
f2_mapped['fiscal_year']   = f2_orig['fiscal_year']
f2_mapped['period']        = np.nan
f2_mapped['category']      = f2_orig['Category / Type']
f2_mapped['line_item']     = f2_orig['Subject / Description']

# Budget rows: the budget amount comes from _amount_zmw
f2_mapped['budget_zmw']    = np.where(budget_mask, f2_orig['_amount_zmw'], np.nan)
f2_mapped['actual_zmw']    = np.nan  # File 2 has no actual figures

# For council minutes: use Key Resolution as description
f2_mapped['description']   = np.where(
    f2_orig['row_type'] == 'council_minutes',
    f2_orig['Key Resolution / Outcome / Value'],
    np.nan
)

f2_mapped['source_document'] = f2_orig['Source Document']
f2_mapped['source_table']    = np.nan
f2_mapped['source_page']     = np.nan
f2_mapped['scope']           = np.nan
f2_mapped['currency']       = 'ZMW'
f2_mapped['ward_or_constituency'] = np.nan
f2_mapped['stakeholders']    = np.nan

# File 2 specific columns
f2_mapped['reference_code']   = f2_orig['Reference / Code']
f2_mapped['key_resolution']   = np.where(
    f2_orig['row_type'] == 'council_minutes',
    f2_orig['Key Resolution / Outcome / Value'],
    np.nan
)
f2_mapped['proposer']         = f2_orig['Proposer']
f2_mapped['seconder']        = f2_orig['Seconder']
f2_mapped['amount_zmw']      = np.where(budget_mask, f2_orig['_amount_zmw'], np.nan)
f2_mapped['budget_year_label'] = f2_orig['_budget_year_label']
f2_mapped['funding_source']  = f2_orig['_funding_source']
f2_mapped['notes']           = f2_orig['Notes']

f2_mapped = f2_mapped[unified_cols]

# ============================================================
# PART 15: COMBINE BOTH FILES
# ============================================================

combined = pd.concat([f1_mapped, f2_mapped], ignore_index=True)

# ============================================================
# PART 16: GENERATE SEQUENTIAL RECORD IDs FOR FILE 2 ROWS
# ============================================================
# File 2 rows have NaN record_id. We generate unique IDs like:
#   KIT2-BR-2026-001, KIT2-CR-2025-002, etc.
# The prefix encodes the record type, followed by fiscal year,
# then a sequential number.

prefix_map = {
    'council_resolution': 'CR', 'council_motion': 'CM',
    'council_proceeding': 'CP',
    'budget_revenue': 'BR', 'budget_expenditure': 'BE',
    'budget_line_item': 'BL',
    'cdf_proposed_project': 'CPS', 'cdf_approved_project': 'CA',
    'cdf_project': 'CD', 'unknown': 'UK'
}

counter = 1
for i in combined.index:
    if pd.isna(combined.at[i, 'record_id']) or str(combined.at[i, 'record_id']).strip() in ('nan', ''):
        rt = str(combined.at[i, 'record_type'])
        fy = str(combined.at[i, 'fiscal_year']) if pd.notna(combined.at[i, 'fiscal_year']) else 'UNK'
        prefix = prefix_map.get(rt, 'UK')
        combined.at[i, 'record_id'] = f'KIT2-{prefix}-{fy}-{counter:03d}'
        counter += 1

# ============================================================
# PART 17: POST-MERGE FIXES
# ============================================================

# Fix 1: Council proceeding rows from the stakeholders meeting had
# no fiscal year — the reference codes (BPM/02/05/25) indicate 2025.
cp_mask = combined['record_type'] == 'council_proceeding'
combined.loc[cp_mask & combined['fiscal_year'].isna(), 'fiscal_year'] = '2025'
# Also fix their record IDs from UNK to 2025
for i in combined[cp_mask].index:
    old_id = str(combined.at[i, 'record_id'])
    combined.at[i, 'record_id'] = old_id.replace('-UNK-', '-2025-')

# Fix 2: "Final.pdf" is actually the 2026 budget document
final_mask = combined['source_document'] == 'Final.pdf'
combined.loc[final_mask, 'source_document'] = '2026-budget-Kitwe-City-Council-amended-Final.pdf'

# Fix 3: CDF approved projects had no fiscal year — they're from 2024 CDF document
cdf_appr_mask = combined['record_type'] == 'cdf_approved_project'
combined.loc[cdf_appr_mask, 'fiscal_year'] = '2024'
for i in combined[cdf_appr_mask].index:
    old_id = str(combined.at[i, 'record_id'])
    combined.at[i, 'record_id'] = old_id.replace('-UNK-', '-2024-')

# ============================================================
# PART 18: FINAL CLEANUP
# ============================================================

# Replace NaN with empty strings for cleaner CSV output
for col in combined.columns:
    combined[col] = combined[col].apply(
        lambda x: '' if pd.isna(x) or str(x).strip() in ('nan', 'NaN', 'None', 'none')
        else str(x).strip()
    )

# Ensure fiscal_year is integer where present
combined['fiscal_year'] = combined['fiscal_year'].apply(
    lambda x: str(int(float(x))) if x != '' and x not in ('UNK', 'nan', '') else x
)

# Remove any completely empty rows
empty_rows = combined.apply(lambda row: all(v == '' for v in row), axis=1)
combined = combined[~empty_rows].reset_index(drop=True)

print(f'\nCombined shape: {combined.shape}')
print(f'Record types: {combined["record_type"].value_counts().to_dict()}')
print(f'Fiscal years: {combined["fiscal_year"].value_counts().to_dict()}')

# ============================================================
# PART 19: REMOVE COLUMNS USER DOESN'T WANT
# ============================================================
# The user requested removal of these columns from the combined file:

remove_cols = [
    'ward_or_constituency', 'currency', 'budget_zmw', 'province',
    'council_name', 'scope', 'reference_code', 'key_resolution',
    'proposer', 'seconder', 'amount_zmw', 'budget_year_label',
    'funding_source', 'notes'
]

drop_cols = [c for c in remove_cols if c in combined.columns]
combined.drop(columns=drop_cols, inplace=True)
print(f'\nDropped {len(drop_cols)} columns: {drop_cols}')
print(f'Remaining columns: {list(combined.columns)}')

# Save combined file
combined.to_csv('outputs/kitwe_city_council_combined.csv', index=False, quoting=1)
print(f'\nSaved combined file: {combined.shape[0]} rows × {combined.shape[1]} columns')

# ============================================================
# PART 20: BUILD DUPLICATES FILE
# ============================================================
# Create a separate file containing ONLY the problematic/overlapping
# rows so the user can compare with the combined file.
#
# Three types of duplicates:
#   1. Empty row removed from File 1 (KIT-EXP-2023-004)
#   2. Overlapping revenue line items (same name in both files,
#      but different values from different source documents)
#   3. Within-file duplicates in File 2 (identical source,
#      subject, and seconder — repeated entries)

# --- Re-load originals for duplicate detection ---
f1_raw = pd.read_csv('uploads/kitwe_city_council_data__1_(1).csv', dtype=str)
f2_raw = pd.read_csv('uploads/DataMining-project.csv', dtype=str)

# Type 1: Empty duplicate row
f1_empty = f1_raw[f1_raw['record_id'] == 'KIT-EXP-2023-004'].copy()
f1_empty['duplicate_reason'] = 'Empty duplicate row (all financial values NaN)'
f1_empty['source_file'] = 'kitwe_city_council_data__1_(1).csv'

# Type 2: Overlapping revenue line items
overlap_names = {'Other Grants', 'Constituency Development Fund',
                 'Local Government Equalisation Fund'}

f1_overlap = f1_raw[f1_raw['line_item'].isin(overlap_names)].copy()
f1_overlap['duplicate_reason'] = (
    'Overlapping revenue line item with File 2 '
    '(same name but from audited actuals source vs budget estimates source)'
)
f1_overlap['source_file'] = 'kitwe_city_council_data__1_(1).csv'

f2_overlap = f2_raw[f2_raw['Subject / Description'].isin(overlap_names)].copy()
f2_overlap['duplicate_reason'] = (
    'Overlapping revenue line item with File 1 '
    '(same name but from budget estimates source vs audited actuals source)'
)
f2_overlap['source_file'] = 'DataMining-project.csv'

# Type 3: Within-file duplicates in File 2
f2_dupe_mask = f2_raw.duplicated(
    subset=['Source Document', 'Subject / Description', 'Seconder'], keep=False
)
f2_dupes = f2_raw[f2_dupe_mask].copy()

# Mark first occurrences vs extra copies
f2_dupe_extra = f2_raw.duplicated(
    subset=['Source Document', 'Subject / Description', 'Seconder'], keep='first'
)
first_occ = ~f2_dupe_extra & f2_dupe_mask

f2_dupes['duplicate_reason'] = (
    'Within-file duplicate in File 2 (identical source, subject, and seconder)'
)
f2_dupes.loc[first_occ, 'duplicate_reason'] = (
    'Within-file duplicate in File 2 (original — first occurrence)'
)
f2_dupes['source_file'] = 'DataMining-project.csv'

print(f'\nDuplicate types:')
print(f'  Type 1 (empty row):           {len(f1_empty)} rows')
print(f'  Type 2 (File 1 overlaps):    {len(f1_overlap)} rows')
print(f'  Type 2 (File 2 overlaps):    {len(f2_overlap)} rows')
print(f'  Type 3 (within-file dupes): {len(f2_dupes)} rows')

# --- Combine all duplicates ---
# Build unified column set (superset of both files + metadata)
all_dup_cols = sorted(set(
    list(f1_raw.columns) + list(f2_raw.columns)
    + ['duplicate_reason', 'source_file']
))

frames = []
for df in [f1_empty, f1_overlap, f2_overlap, f2_dupes]:
    for col in all_dup_cols:
        if col not in df.columns:
            df[col] = ''
    df_out = df[all_dup_cols].copy()
    frames.append(df_out)

all_dups = pd.concat(frames, ignore_index=True)

# Merge duplicate_reason into description so it doesn't sit in its own column
all_dups['description'] = all_dups.apply(
    lambda r: (r['duplicate_reason'] + ' | ' + r['description']).strip(' | ')
    if r.get('duplicate_reason', '') and r.get('description', '')
    else (r.get('duplicate_reason', '') or r.get('description', '')),
    axis=1
)

# Drop extra metadata columns and File 2 original columns not in combined schema
extra_to_drop = [c for c in all_dups.columns if c not in combined.columns]
all_dups.drop(columns=extra_to_drop, inplace=True)

# Ensure same column order as combined file
all_dups = all_dups[list(combined.columns)]

# Clean NaN
for col in all_dups.columns:
    all_dups[col] = all_dups[col].apply(
        lambda x: '' if pd.isna(x) or str(x).strip() in ('nan', 'NaN', 'None', 'none')
        else str(x).strip()
    )

print(f'\nDuplicates file shape: {all_dups.shape}')
print('Breakdown by reason:')
for reason, count in all_dups['description'].str.extract(r'^(.+?)(?:\s*\|)?', expand=False).value_counts().items():
    if reason:
        print(f'  {count:4d} | {reason}')

# Save duplicates file
all_dups.to_csv('outputs/kitwe_city_council_data__1_(1).csv', index=False, quoting=1)
print(f'\nSaved duplicates file: {all_dups.shape[0]} rows × {all_dups.shape[1]} columns')

# ============================================================
# FINAL SUMMARY
# ============================================================
print('\n' + '=' * 60)
print('PIPELINE COMPLETE')
print('=' * 60)
print(f'Combined file:   {combined.shape[0]} rows × {combined.shape[1]} columns')
print(f'Duplicates file:  {all_dups.shape[0]} rows × {all_dups.shape[1]} columns')
print(f'Columns:          {list(combined.columns)}')


# ============================================================
# ENRICHMENT: Extract Proposer/Seconder/Approved/Budget from
# the combined raw source file (kitwe_combined_dataset.csv)
# ============================================================
print('
' + '=' * 60)
print('ENRICHMENT MERGE')
print('=' * 60)

raw_enrich = pd.read_csv('data/raw/kitwe_combined_dataset.csv')
raw_only = raw_enrich[raw_enrich['record_id'].isna()].copy()

# --- Classify the Seconder column (mixed semantics) ---
def classify_seconder(val):
    if pd.isna(val):
        return {'seconder_name': np.nan, 'funding_source': np.nan,
                'budget_amount_zmw': np.nan, 'approved': np.nan}
    s = str(val).strip()
    if 'Councillor' in s or 'Mayor' in s or 'Worship' in s:
        return {'seconder_name': s, 'funding_source': np.nan,
                'budget_amount_zmw': np.nan, 'approved': np.nan}
    if 'CDF' in s:
        return {'seconder_name': np.nan, 'funding_source': s,
                'budget_amount_zmw': np.nan, 'approved': np.nan}
    if s == 'Approved project':
        return {'seconder_name': np.nan, 'funding_source': np.nan,
                'budget_amount_zmw': np.nan, 'approved': 'Yes'}
    if s in ('0', '0.0'):
        return {'seconder_name': np.nan, 'funding_source': np.nan,
                'budget_amount_zmw': 0.0, 'approved': np.nan}
    try:
        amt = float(s)
        return {'seconder_name': np.nan, 'funding_source': np.nan,
                'budget_amount_zmw': amt, 'approved': np.nan}
    except ValueError:
        pass
    return {'seconder_name': np.nan, 'funding_source': np.nan,
            'budget_amount_zmw': np.nan, 'approved': np.nan}

classified = raw_only['Seconder'].apply(lambda x: pd.Series(classify_seconder(x)))
raw_only = pd.concat([raw_only, classified], axis=1)
raw_only['budget_year_label'] = raw_only['Amount (K)']
raw_only['proposer_name'] = raw_only['Proposer']

# --- Positional matching ---
raw_only['match_key'] = (raw_only['Source Document'].str.strip().str.lower() + '||' +
                        raw_only['Subject / Description'].str.strip().str.lower())
combined['match_key'] = (combined['source_document'].str.strip().str.lower() + '||' +
                        combined['line_item'].str.strip().str.lower())

raw_only['_pos'] = raw_only.groupby('match_key').cumcount()
combined['_pos']   = combined.groupby('match_key').cumcount()

enrich_cols = ['match_key','_pos','proposer_name','seconder_name',
              'funding_source','budget_amount_zmw','approved','budget_year_label']
combined = combined.merge(raw_only[enrich_cols], on=['match_key','_pos'], how='left')
combined.drop(columns=['match_key','_pos'], inplace=True)

# Post-merge fixes
cdf_mask = combined['funding_source'].notna()
combined.loc[cdf_mask & combined['approved'].isna(), 'approved'] = 'No'
combined.loc[combined['record_type']=='cdf_approved_project', 'approved'] = 'Yes'

combined['budget_amount_zmw'] = pd.to_numeric(combined['budget_amount_zmw'], errors='coerce')

print(f'Enrichment complete. Shape: {combined.shape}')
print('Non-null counts:')
for c in ['proposer_name','seconder_name','funding_source','budget_amount_zmw','approved','budget_year_label']:
    print(f'  {c}: {combined[c].notna().sum()}')

# --- Re-export all thematic CSVs with enrichment columns ---
for fname, rtypes in THEMATIC_MAP.items():
    subset = combined[combined['record_type'].isin(rtypes)].copy()
    out_path = f'data/processed/db-unza26-csc4792-{fname}.csv'
    subset.to_csv(out_path, index=False, sep='|', quoting=1)
    print(f'  Re-exported {fname}: {len(subset)} rows')

combined.to_csv('data/processed/db-unza26-csc4792-full_dataset.csv',
               index=False, sep='|', quoting=1)
print(f'
Re-exported full_dataset: {combined.shape}')

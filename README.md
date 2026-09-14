# Kitwe City Council Digital Footprint Dataset

**Course:** CSC4792 — University of Zambia (UNZA), 2026  
**Instructor:** Lighton Phiri (lighton.phiri@gmail.com)  
**Council:** Kitwe City Council, Copperbelt Province, Zambia

---

## Overview

This repository contains a comprehensive dataset constructed from the digital footprints of **Kitwe City Council**, one of the principal local authorities in Zambia's Copperbelt Province. The dataset consolidates publicly available council documents — including budget revenue and expenditure tables, CDF (Constituency Development Fund) project records, council meeting resolutions, annual financial statements, debt arrears data, and empowerment grant records — into a unified, pipe-separated CSV format suitable for analysis and reproducible research.

The dataset was constructed as part of a data-mining assignment for CSC4792 at the University of Zambia, following a multi-source extraction, cleaning, and integration methodology.

## Dataset Description

- **Total records:** 963 rows (after deduplication)
- **Columns:** 18 (record_id, record_type, fiscal_year, period, category, line_item, actual_zmw, description, source_document, source_table, source_page, stakeholders, proposer_name, seconder_name, funding_source, budget_amount_zmw, approved, budget_year_label)
- **Record types:** 17 (e.g., revenue, expenditure, cdf_project, council_resolution, financial_statement, debt_arrears, etc.)
- **Fiscal years:** 2018–2026
- **Currency:** ZMW (Zambian Kwacha)
- **Separator:** Pipe (`|`)
- **Naming convention:** `db-unza26-csc4792-[DESCRIPTION].csv`

## Repository Structure

```
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
├── data/
│   ├── raw/                         # Original source CSV files
│   │   ├── kitwe_city_council_data__1_(1).csv
│   │   ├── DataMining-project.csv
│   │   └── kitwe_combined_dataset.csv
│   └── processed/                   # Cleaned, thematic CSV datasets
│       ├── db-unza26-csc4792-full_dataset.csv
│       ├── db-unza26-csc4792-budget_revenue.csv
│       ├── db-unza26-csc4792-budget_expenditure.csv
│       ├── db-unza26-csc4792-cdf_projects.csv
│       ├── db-unza26-csc4792-council_resolutions.csv
│       ├── db-unza26-csc4792-financial_statements.csv
│       ├── db-unza26-csc4792-debt_arrears.csv
│       ├── db-unza26-csc4792-empowerment_grants.csv
│       └── db-unza26-csc4792-duplicates.csv
├── notebooks/
│   └── db-unza26-csc4792-notebook.ipynb   # Full Jupyter Notebook pipeline
├── scripts/
│   └── kitwe_city_council_cleaning_pipeline.py  # 20-step cleaning + enrichment script
└── docs/
    └── db-unza26-csc4792-data_description_paper.md  # Data in Brief paper
```

## Thematic Files

| File | Records | Description |
|------|---------|-------------|
| `db-unza26-csc4792-cdf_projects.csv` | 387 | Constituency Development Fund project records |
| `db-unza26-csc4792-budget_revenue.csv` | 235 | Revenue budget line items |
| `db-unza26-csc4792-budget_expenditure.csv` | 213 | Expenditure budget line items |
| `db-unza26-csc4792-council_resolutions.csv` | 88 | Council meeting resolutions |
| `db-unza26-csc4792-financial_statements.csv` | 23 | Annual financial statement summaries |
| `db-unza26-csc4792-debt_arrears.csv` | 13 | Debt and arrears records |
| `db-unza26-csc4792-empowerment_grants.csv` | 4 | Empowerment grant allocations |
| `db-unza26-csc4792-full_dataset.csv` | 963 | Complete deduplicated dataset |
| `db-unza26-csc4792-duplicates.csv` | 120 | Records removed as duplicates |

## How to Run

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/db-unza26-csc4792-kitwe-city-council.git
cd db-unza26-csc4792-kitwe-city-council
pip install -r requirements.txt
```

### Running the Notebook

```bash
jupyter notebook notebooks/db-unza26-csc4792-notebook.ipynb
```

### Running the Cleaning Pipeline

```bash
python scripts/kitwe_city_council_cleaning_pipeline.py
```

## Data Description Paper

A full data description paper following the **Data in Brief** journal template is included in `docs/`. It covers:
- Specifications table
- Value of the data
- Detailed data description and column schema
- Methods (acquisition, extraction, 20-step cleaning pipeline, integration, deduplication)
- Limitations and ethical considerations

## Kaggle Dataset

The dataset is also published on Kaggle: [Link to be added after upload]

## Acknowledgements

- Kitwe City Council for publishing council documents in the public domain.
- Lighton Phiri, CSC4792 course instructor, University of Zambia.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contact

For questions regarding this dataset, contact the course instructor: Lighton Phiri (lighton.phiri@gmail.com)

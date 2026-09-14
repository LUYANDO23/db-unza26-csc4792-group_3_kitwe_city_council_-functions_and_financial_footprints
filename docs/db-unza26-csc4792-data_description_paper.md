**A Multi-Source Dataset for Kitwe City Council\
Financial Governance Analysis (2018--2026)**

\[Your Name\]^1^, \[Your Co-author if applicable\]\
^1^University of Zambia, School of Computing, Department of Computer
Science, Lusaka, Zambia\
Corresponding author email: your.email\@unza.zm

Abstract {#abstract .unnumbered}
========

This data article presents a multi-source dataset constructed from the
digital footprints of Kitwe City Council, the largest local authority in
Zambia's Copperbelt Province. The dataset comprises 963 structured
records across 18 columns extracted from 21 source documents---including
approved budget estimates, audited financial statements, council meeting
minutes, Constituency Development Fund (CDF) project registers, CDF
empowerment grant records, and budget performance reports---spanning
fiscal years 2018 to 2026. Records are organised into seven thematic
sub-datasets: CDF projects (387 records), budget revenue (235 records),
budget expenditure (213 records), council resolutions (88 records),
financial statements (23 records), debt arrears (13 records), and
empowerment grants (4 records). The dataset is grounded in Zambia's
Local Government Act No. 2 of 2019 and its subsequent amendments (Act 8
of 2023 on LGEF reform; Act 5 of 2026 on CDF allocation of K40 million
per constituency). All files use pipe-separated values with the naming
convention `db-unza26-csc4792-[DESCRIPTION].csv`. The dataset supports
analysis of local government revenue mobilisation, CDF project
implementation patterns, budget adherence, council decision-making
processes, and debt management trends in Zambian local authorities.

**Keywords:** Kitwe City Council; Local Government Act; Constituency
Development Fund; Budget estimates; Audited financial statements;
Council minutes; Copperbelt Province; Zambia; Local governance data;
Municipal finance

Specifications Table {#specifications-table .unnumbered}
====================

\>p4cmX **Subject** & Social Sciences --- Public Administration and
Local Governance\
**Specific subject area** & Municipal finance, local government
budgeting, CDF project implementation, council decision-making\
**Type of data** & Structured tabular data (CSV files)\
**Data format** & Pipe-separated values (CSV with `|` delimiter), quoted
fields\
**How data was acquired** & Manual extraction from audited financial
statements and budget performance reports; programmatic extraction
(`pdfplumber`, `tabula-py`, `python-docx`) from budget PDFs, CDF project
lists, and council minutes\
**Data source location** & Kitwe City Council, Kitwe District,
Copperbelt Province, Zambia (12.8S, 28.2E)\
**Data accessibility** & Repository: Kaggle
([https://www.kaggle.com/datasets/\[username\]/kitwe-city-council-dataset](https://www.kaggle.com/datasets/[username]/kitwe-city-council-dataset));
Code: GitHub
([https://github.com/\[username\]/kitwe-city-council-data](https://github.com/[username]/kitwe-city-council-data))\
**Related research article** & This is a data description article; no
associated research article at time of publication\

Value of the Data
=================

1.  **Local government financial transparency.** The dataset provides
    the first publicly available structured extraction of Kitwe City
    Council's budget estimates, audited actuals, and financial
    statements spanning eight fiscal years (2018--2026). This enables
    longitudinal analysis of revenue mobilisation, expenditure patterns,
    and budget adherence in Zambia's second-largest city.

2.  **CDF implementation tracking.** With 387 records covering proposed,
    approved, and contracted CDF projects, the dataset offers granular
    visibility into how Constituency Development Fund
    allocations---recently increased to K40 million per constituency
    under Amendment Act 5 of 2026---are planned, approved, and
    implemented across Kitwe's constituencies (Chimwemwe, Kamfinsa,
    Wusakile, Nkana, Kwacha).

3.  **Council governance documentation.** The 88 council resolution,
    motion, and proceeding records extracted from meeting minutes
    provide a structured record of council decision-making, including
    proposer/seconder attribution and reference codes---enabling
    research into local democratic processes and accountability.

4.  **LGEF utilisation analysis.** Revenue records from 2018--2026
    explicitly track Local Government Equalisation Fund (LGEF)
    disbursements, enabling analysis of intergovernmental fiscal
    transfer effectiveness following the 2023 LGEF reform (Act 8 of
    2023).

5.  **Debt and arrears monitoring.** The debt arrears sub-dataset (13
    records) captures outstanding obligations to utilities (ZESCO,
    ZAMTEL), statutory bodies (NAPSA, ZRA), and staff, supporting
    research into municipal debt sustainability.

6.  **Reuse potential.** Researchers studying Zambian local governance,
    comparative municipal finance across African local authorities, CDF
    effectiveness, or the impact of legislative reform on local
    government operations can reuse this dataset. The dataset also
    serves as a benchmark for data mining and information extraction
    from semi-structured government documents.

Data Description
================

Dataset Overview
----------------

The dataset consists of 963 structured records distributed across seven
thematic CSV files and one combined file, all using pipe (`|`) as the
field separator. The naming convention follows
`db-unza26-csc4792-[DESCRIPTION].csv` where `[DESCRIPTION]` identifies
the thematic content.

Column Schema
-------------

Each CSV file shares the following 18-column schema (the initial 12
columns plus 6 enrichment columns added during integration):

::: {#tab:schema}
  **Column**            **Type**   **Description**
  --------------------- ---------- -----------------------------------------------------------------------------------------------------------------
  `record_id`           String     Unique identifier: `KIT-[TYPE]-[YEAR]-[SEQ]` (File 1) or `KIT2-[TYPE]-[YEAR]-[SEQ]` (File 2)
  `record_type`         String     Category of the record (17 types)
  `fiscal_year`         Integer    Zambian government fiscal year
  `period`              String     Temporal granularity: FY2018, Q1--Q2, Jan-26, etc.
  `category`            String     Sub-classification within the record type
  `line_item`           String     Descriptive name of the budget line, project, or agenda item
  `actual_zmw`          Float      Monetary amount in Zambian Kwacha; empty for budget estimates and CDF projects without amounts
  `description`         String     Supplementary detail (contract dates, audit notes, outcomes)
  `source_document`     String     Filename of the original PDF/DOCX source
  `source_table`        String     Name of the table within the source document
  `source_page`         String     Page number in the source document
  `stakeholders`        String     Relevant parties (e.g., Kitwe City Council, Wusakile Constituency Cooperatives)
                                   
  `proposer_name`       String     Name of the councillor who proposed a council resolution or motion (54 of 57 resolutions; 26 of 27 motions)
  `seconder_name`       String     Name of the councillor who seconded a resolution or motion (54 of 57; 26 of 27)
  `funding_source`      String     CDF funding label, e.g. "2024 CDF funding" (332 CDF proposed projects)
  `budget_amount_zmw`   Float      Actual budget line amount in ZMW; populated for 164 revenue and 188 expenditure lines
  `approved`            String     "Yes" for CDF approved projects (34), "No" for proposed (332); NaN otherwise
  `budget_year_label`   String     Budget classification label, e.g. "2023 Approved Budget", "2025 Budget Estimate" (164 revenue, 188 expenditure)

  : Column schema for all CSV files.
:::

Record Types
------------

The 17 record types are organised into seven thematic groups:

**CDF Projects (387 records):** CDF proposed projects (332) list
community development projects submitted for Constituency Development
Fund consideration; CDF approved projects (34) record projects that
received formal CDF allocation; CDF projects (21) document
signed/contracted projects with execution details.

**Budget Revenue (235 records):** Budget revenue (164) contains approved
revenue estimates; revenue (23) records audited actual revenue figures;
local revenue (6) captures locally generated revenue sources; revenue
line annual (42) provides annual revenue line-item performance data.

**Budget Expenditure (213 records):** Budget expenditure (189) contains
approved expenditure estimates; expenditure (10) records audited actual
expenditure; expenditure line annual (14) provides annual expenditure
line-item performance data.

**Council Resolutions (88 records):** Council resolutions (57) capture
formally adopted decisions; council motions (27) record proposed but
potentially unresolved items; council proceedings (4) document meeting
agenda items.

**Financial Statements (23 records):** Annual financial statements (22)
summarise audited cash receipts and payments; audit queries (1) flag
outstanding audit findings.

**Debt Arrears (13 records):** Outstanding debt obligations to ZESCO,
ZAMTEL, NAPSA, ZRA, and staff.

**Empowerment Grants (4 records):** CDF empowerment grant allocations to
cooperatives across Kitwe's five constituencies.

Fiscal Year Coverage
--------------------

::: {#tab:fiscal}
    **Fiscal Year** **Records**   **Key Sources**
  ----------------- ------------- ----------------------------------------------------------------------------------
               2018 9             Kitwe-City-Council-2018-FS.pdf
               2019 9             Kitwe-City-Council-2019-FS.pdf
               2020 9             Kitwe-City-Council-2020-FS.pdf
               2021 9             Kitwe-City-Council-2021-FS.pdf
               2022 60            Kitwe-C-C-2022-Financial-Statements-SIGNED.pdf, Budget-Estimates-2023.pdf
               2023 158           Financial statements, Budget-Estimates-2023.pdf, Council minutes (3 files)
               2024 448           CDF-2024-PROPOSED-AND-APPROVED-PROJECTS.pdf, Financial statements
               2025 207           Approved-Budget-2025.pdf, Budget-Performance-Report-116-LAs.pdf, Council minutes
               2026 54            2026-budget-Kitwe-City-Council-amended-Final.pdf, CDF signing records

  : Record distribution by fiscal year.
:::

Methods
=======

Data Acquisition
----------------

Source documents were obtained from two primary channels:

1.  **Kitwe City Council official website**
    (<https://www.kitwecitycouncil.gov.zm>): Budget estimates, financial
    statements, and council news were downloaded directly.

2.  **Ministry of Local Government and Rural Development** portal:
    Budget performance reports and standardised financial statement
    templates were obtained from the Ministry's public document
    repository.

A total of 21 source documents were collected, comprising 14 PDFs, 3
DOCX files, 3 images/semi-structured documents, and 1 web page. The
documents span fiscal years 2018 to 2026.

Data Extraction
---------------

Two complementary extraction approaches were employed:

**File 1 --- Manual curation from audited sources.** The first source
file (`kitwe_city_council_data__1__(1).csv`, 157 rows $\times$ 18
columns) was manually constructed by reading audited financial
statements (2018--2024) and the Budget Performance Report for 116 Local
Authorities. Manual extraction was necessary because audited financial
statements use non-standard table layouts that resisted automated
parsing---tables span multiple pages, use merged cells, and employ
inconsistent column ordering across years.

**File 2 --- Programmatic data mining.** The second source file
(`DataMining-project.csv`, 807 rows $\times$ 9 columns) was extracted
programmatically using Python libraries:

-   `pdfplumber` and `tabula-py` for table extraction from budget
    estimate PDFs and CDF project lists

-   `python-docx` for structured text extraction from council minutes
    DOCX files

-   Regular expressions for parsing reference codes, fiscal year labels,
    and monetary amounts

Data Cleaning
-------------

The cleaning pipeline involved 20 documented steps organised into three
phases:

**Phase 1: File 1 cleaning (Steps 1--7)**

1.  Detected and corrected column misalignment caused by an undocumented
    `description` field in File 1 that shifted `source_document` through
    `scope` rightward by one column.

2.  Removed one empty duplicate row (KIT-EXP-2023-004) where all
    financial values were NaN.

3.  Filled missing `line_item` values by copying from the `category`
    column.

4.  Fixed a row where `source_document = ‘27’` was a leaked page number;
    restored the correct source document.

5.  Fixed a row where `source_page = ‘10/09/2026’` was a leaked date;
    restored page number and appended the date to the description.

6.  Converted `budget_zmw` and `actual_zmw` to numeric types.

7.  Stripped whitespace from all text columns.

**Phase 2: File 2 cleaning (Steps 8--14)**

8.  Classified each row into one of three semantic types based on the
    source document filename.

9.  Remapped misaligned columns: budget rows had amounts in `Seconder`
    and year labels in `Amount (K)`; CDF rows had funding source text in
    `Seconder`.

10. Fixed leaked source document filenames in the `Notes` column.

11. Fixed leaked budget document text in the `Amount (K)` column.

12. Extracted fiscal year from three sources depending on row type:
    budget year label, CDF funding source text, or council minutes
    filename.

13. Mapped File 2's `Category / Type` values to the unified record type
    vocabulary.

14. Standardised the disabilities stakeholders meeting filename across
    inconsistent references.

**Phase 3: Post-merge fixes (Steps 15--20)**

15. Populated missing fiscal years for council proceedings (reference
    codes BPM/02/05/25 indicate 2025).

16. Corrected `source_document = ‘Final.pdf’` to the full filename.

17. Assigned fiscal year 2024 to CDF approved projects.

18. Replaced all remaining NaN values with empty strings for clean CSV
    output.

19. Converted fiscal year to integer where present.

20. Removed any completely empty rows.

Data Integration
----------------

The two source files were merged into a unified 26-column superset
schema, with empty placeholders for columns not present in each file.
After integration, 14 columns with minimal data were dropped, yielding
the final 12-column schema, to which six enrichment columns were
subsequently added (see Section 3.5).

Deduplication
-------------

Three types of duplicate/overlapping records were identified and
catalogued in a separate file (`db-unza26-csc4792-duplicates.csv`, 120
records):

1.  **Empty duplicate row** (1 record): KIT-EXP-2023-004 with all
    financial values as NaN---removed from the combined dataset.

2.  **Cross-file overlaps** (103 records): Revenue line items appearing
    in both files with different monetary values---File 1 reports
    audited actuals while File 2 reports budget estimates. Retained
    because they are semantically distinct.

3.  **Within-file duplicates** (16 records): 8 pairs of rows with
    identical source document, subject, and seconder values. First
    occurrences retained; duplicates moved to the duplicates file.

Enrichment Merge
----------------

An additional raw source file (`kitwe_combined_dataset.csv`, 1770 rows
$\times$ 32 columns) contained supplementary fields not captured in the
initial extraction pipeline. Key observations about the raw enrichment
data:

1.  The `Proposer` column contains councillor names for council
    resolutions and motions (80 non-null rows).

2.  The `Seconder` column has **mixed semantics**: councillor names (80
    rows), CDF funding labels such as "2024 CDF funding" (332 rows),
    approval flags "Approved project" (33 rows), numeric budget amounts
    (340 rows), and zeros (13 rows).

3.  The `Amount (K)` column is misleadingly named---it contains budget
    *year labels* (e.g., "2023 Approved Budget", "2025 Budget
    Estimate"), not monetary amounts. The actual monetary amounts for
    budget lines are stored in the `Seconder` column, indicating a
    column misalignment in the original extraction.

A classification function was applied to `Seconder` to decompose it into
four distinct enrichment fields (`seconder_name`, `funding_source`,
`budget_amount_zmw`, `approved`). The `Amount (K)` column was mapped to
`budget_year_label` and `Proposer` to `proposer_name`.

Positional matching within duplicate `match_key` groups (concatenation
of source document and line item, case-insensitive) was required because
CDF projects and council motions often share identical descriptions
(e.g., eight rows of "Construction of Wall Fence"). Two duplicate rows
arising from budget misalignment (KIT2-BR-2026-216 and KIT2-CA-2024-807)
were deduplicated, retaining the row with populated data.

Post-merge corrections included setting `approved = ‘Yes’` for all CDF
approved project records and `approved = ‘No’` for all CDF proposed
project records with a non-null `funding_source`.

Thematic Splitting
------------------

The 963-record combined dataset was partitioned into seven thematic CSV
files based on record type mappings.

All files use pipe (`|`) as the field separator and are named following
the convention `db-unza26-csc4792-[DESCRIPTION].csv`.

Limitations
===========

1.  **Temporal gaps:** Financial statement records for 2018--2021
    contain only summary-level receipts and payments (9 records per
    year), whereas years 2022--2024 have more granular line-item data.
    This limits comparability across all fiscal years.

2.  **Missing budget actuals:** The `actual_zmw` column is populated
    primarily for records from audited financial statements (File 1) and
    is empty for budget estimates (File 2). Comparative analysis of
    budget vs. actual requires joining across the two source types.

3.  **Council minutes coverage:** Only three council meeting minutes
    documents (October 2023, April 2023, June 2023) and one stakeholders
    meeting were available digitally. Council decisions from other
    periods are not represented.

4.  **Debt arrears point-in-time:** The debt arrears sub-dataset
    reflects obligations at a single point in time (Q1--Q2 2025) and
    does not track arrears trajectories over time.

5.  **Monetary precision:** All ZMW amounts are stored as floating-point
    numbers, which may introduce rounding artifacts for very large
    figures.

6.  **Single-council scope:** The dataset covers only Kitwe City Council
    and cannot be generalised to all Zambian local authorities without
    additional data collection.

Ethical Considerations
======================

All source documents used in this dataset are publicly available from
the Kitwe City Council website and the Ministry of Local Government and
Rural Development portal. No confidential, personal, or
restricted-access data was used. Council minutes contain the names of
elected councillors and council officers in their official capacities;
these are matters of public record per Zambia's Constitution and the
Local Government Act. The `proposer_name` and `seconder_name` enrichment
columns derive directly from these public records. No personal data of
private citizens is included.

CRediT Author Statement {#credit-author-statement .unnumbered}
=======================

-   **\[Your Name\]:** Conceptualisation, Methodology, Software, Data
    curation, Writing --- original draft, Writing --- review & editing,
    Visualisation

-   **\[Co-author if applicable\]:** Supervision, Writing --- review &
    editing

Declaration of Competing Interest {#declaration-of-competing-interest .unnumbered}
=================================

The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to
influence the work reported in this paper.

Acknowledgements {#acknowledgements .unnumbered}
================

This work was completed as part of CSC 4792 (Data Mining and Knowledge
Discovery) at the University of Zambia, under the supervision of
Dr. Lighton Phiri. We acknowledge Kitwe City Council for making their
financial documents publicly accessible online.

Data Availability {#data-availability .unnumbered}
=================

The dataset is publicly available on Kaggle:
[https://www.kaggle.com/datasets/\[username\]/kitwe-city-council-dataset](https://www.kaggle.com/datasets/[username]/kitwe-city-council-dataset)

The source code for data extraction, cleaning, and integration is
available on GitHub:
[https://github.com/\[username\]/kitwe-city-council-data](https://github.com/[username]/kitwe-city-council-data)

References {#references .unnumbered}
==========

1.  Government of Zambia, *Local Government Act No. 2 of 2019*, Lusaka:
    Government Printer, 2019.

2.  Government of Zambia, *Local Government (Amendment) Act No. 8 of
    2023*, Lusaka: Government Printer, 2023.

3.  Government of Zambia, *Local Government (Amendment) Act No. 5 of
    2026*, Lusaka: Government Printer, 2026.

4.  Kitwe City Council, *Approved Budget Estimates FY2025*, Kitwe, 2025.
    Available: <https://www.kitwecitycouncil.gov.zm>

5.  Kitwe City Council, *CDF Proposed and Approved Projects 2024*,
    Kitwe, 2024. Available: <https://www.kitwecitycouncil.gov.zm>

6.  Ministry of Local Government and Rural Development, *Budget
    Performance Report for 116 Local Authorities*, Lusaka, 2025.

7.  L. Phiri, "A Multi-source Dataset for CS1 Failure Prediction," *Data
    in Brief*, vol. 42, 2022. DOI: 10.1016/j.dib.2022.108274

8.  Auditor General of Zambia, *Report on the Accounts of Local
    Authorities*, Lusaka, various years 2018--2024.

# sales-data-sanitizer
A Python-driven data cleaning, normalization, and automated quality validation pipeline designed to fix and sanitize messy retail/cafe sales datasets.

#  Cafe Sales Data Cleaning & Validation Pipeline

An end-to-end Python pipeline designed to process, clean, and validate messy transactional datasets (e.g., `dirty_cafe_sales.csv`). It resolves missing values, eliminates duplicate entries, normalizes text fields, and applies strict rule-based data quality checks to ensure data integrity for analytics.

---

##  Key Features

- ** Data Cleaning & Preprocessing:**
  - Removes duplicate records.
  - Imputes missing categorical values using the **mode** and numerical fields using the **median**.
  - Standardizes column headers and converts strings to numeric/datetime types.
  - Normalizes text entries (e.g., correcting typos like `cofee` ➔ `coffee`).

- ** Comprehensive Data Validation:**
  - **Numeric Checks:** Verifies positive pricing and quantity constraints[cite: 2].
  - **Calculation Verification:** Validates line-item math (`Total Spent` == `Price Per Unit` * `Quantity`)[cite: 2].
  - **Temporal Integrity:** Ensures dates are properly formatted and flags non-historical/future transaction dates[cite: 2].
  - **Categorical Compliance:** Validates against known allowed payment methods[cite: 2].

- ** Before vs. After Quality Reporting:**
  - Calculates percentage improvement in missing values and invalid rows[cite: 2].
  - Generates expectation success summaries and terminal-based status reports using **Rich**[cite: 2].

---

##  Tech Stack

- **Language:** Python 3.x
- **Data Wrangling:** `pandas`, `numpy`[cite: 2]
- **Terminal UI / Reporting:** `rich`[cite: 2]

---

##  Getting Started

### 1. Installation
Install the required Python dependencies:

```bash
pip install pandas numpy rich

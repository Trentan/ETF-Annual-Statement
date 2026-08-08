# ETF & Share Dividend Statement Parser for GnuCash

Automated extraction, tax component splitting, and consolidation of Australian ETF Annual Tax Statements and Individual Share Dividend Advices for import into GnuCash.

---

## Quick Start (How-To Guide)

### 1. Process ETF Annual Tax Statements

Place your annual PDF tax statements (Vanguard, BetaShares, GlobalX, VanEck, iShares) into `Tax\Statements\`, then run:

```powershell
python etf2cb_runFolder.py
python etfcb_mergeSplits.py
```

- **`etf2cb_runFolder.py`**: Scans all PDF statements in `Tax\Statements\`, extracts component tables via Tabula, and generates individual `*_split.csv` files.
- **`etfcb_mergeSplits.py`**: Validates double-entry transaction balances, formats header rows, and consolidates all ETF splits into:
  `Tax\combined_split_statements.csv`

---

### 2. Process Individual Company Dividend Statements

Place individual share dividend PDF advices (e.g. ASK, CSL, DMP, GYG, SOL, WTC) into `Tax\IndidividualPayments\`, then run:

```powershell
python process_individual_payments.py
```

- **`process_individual_payments.py`**: Dynamically extracts franked dividends, unfranked income, franking credits, and cash payment amounts without hardcoded values.
- Generates a separate, ready-to-import CSV at:
  `Tax\IndidividualPayments\individual_payments_splits.csv`

---

## Double-Entry Accounting & Clearing Account Setup

### Why `Equity:Clearing:Distribution` is Used

In double-entry bookkeeping (especially for trusts), annual tax statements reclassify cash received during the year into specific ATO tax return categories (`13C`, `13U`, `18H`, `20E/20M`, etc.).

To prevent direct debit transactions from cluttering your parent `Income:Distribution` account, cash balancing splits are mapped to a dedicated clearing account: **`Equity:Clearing:Distribution`** (configured in `tax-acc.csv`).

#### How the Workflow Functions:

1. **During the Financial Year (Quarterly Payouts)**:
   When cash payouts land in your bank account, record them as:
   - **Debit**: `Asset:Bank` (Cash received)
   - **Credit**: `Equity:Clearing:Distribution`

2. **At Year-End (Annual Tax Statement Import)**:
   Importing the CSV split transactions:
   - **Credits** your tax income sub-accounts (`13C`, `13U`, `18H`, `20E/20M`) with gross tax income.
   - **Debits** `Equity:Clearing:Distribution` by the net cash amount, **clearing out the clearing account to exactly `$0.00`**.

3. **Result at Book Closing**:
   - `Equity:Clearing:Distribution` balance = **`$0.00`**
   - Parent `Income:Distribution` contains **zero direct debit clutter**, preserving clean gross tax income sub-account balances for trust tax return preparation and beneficiary distributions.

---

## Standard Tax Account Mapping Reference

Tax component account mappings are configured in `tax-acc.csv`:

| Tax Code / Label | Description | Account Type | GnuCash Chart of Accounts |
| :--- | :--- | :---: | :--- |
| **13C** | Franked Distributions | Credit | `Income:Distribution:13C` |
| **13Q** | Franking Credits Offset | Credit | `Income:Distribution:13Q` |
| **13U** | Unfranked Distributions (CFI) | Credit | `Income:Distribution:13U` |
| **18H** | Capital Gains (18A Net + GrossUp) | Credit | `Income:Distribution:18H` |
| **20E / 20M** | Assessable Foreign Source Income | Credit | `Income:Distribution:20E/20M` |
| **20F** | NZ Franking Credits | Credit | `Income:Distribution:20F` |
| **20O** | Foreign Income Tax Offset (FITO) | Credit | `Income:Distribution:20O` |
| **Cost Base** | AMIT Cost Base Increase / Decrease | Debit / Credit | `Asset:Shares:CostBase` |
| **Cash Payout** | Net Distribution Paid | Debit | `Equity:Clearing:Distribution` |
| **Rounding** | Balancing Residual Adjustment | Credit | `Income:Distribution:Rounding` |

---

## Sample Multi-Split CSV Output

### ETF Annual Statement Split Example (VDHG)

```csv
Entity,Date,Description,Account,Deposit
X******6135,30/06/2026,VDHG,Income:Distribution:13U,-344.25
X******6135,30/06/2026,VDHG,Income:Distribution:13C,-399.27
X******6135,30/06/2026,VDHG,Income:Distribution:13Q,127.33
X******6135,30/06/2026,VDHG,Income:Distribution:18H:18A,-471.73
X******6135,30/06/2026,VDHG,Income:Distribution:18H:GCTGrossUp,-471.73
X******6135,30/06/2026,VDHG,Income:Distribution:20E/20M,-449.63
X******6135,30/06/2026,VDHG,Income:Distribution:20O,48.42
X******6135,30/06/2026,VDHG,Asset:Shares:CostBase,297.34
X******6135,30/06/2026,VDHG,Equity:Clearing:Distribution,1663.52
```

### Individual Share Dividend Split Example (SOL)

```csv
Entity,Date,Description,Account,Deposit
X******6135,14/05/2026,SOL,Income:Distribution:13C,-637.44
X******6135,14/05/2026,SOL,Income:Distribution:13Q,-273.19
X******6135,14/05/2026,SOL,Asset:TaxCredits:Franking,273.19
X******6135,14/05/2026,SOL,Equity:Clearing:Distribution,637.44
```

---

## Importing into GnuCash

1. Open GnuCash and select **File -> Import -> Import Transactions from CSV...**
2. Choose either `Tax\combined_split_statements.csv` or `Tax\IndidividualPayments\individual_payments_splits.csv`.
3. Set **Leading lines to skip: 1** and select **Multi-split**.
4. Set **Date Format: d-m-y**.
5. Map CSV columns:
   - Column 1 -> **Entity**
   - Column 2 -> **Date**
   - Column 3 -> **Description**
   - Column 4 -> **Account**
   - Column 5 -> **Deposit**
6. Map GnuCash Account IDs to your Chart of Accounts and click **Apply**.

---

## License

This project is licensed under the terms of the GNU GPLv3 license.

# QuickPizza API Testing with pytest and requests

This repository contains automated API test suites for **QuickPizza** (`https://quickpizza.grafana.com`) as part of the ITDS362 Software Quality Assurance and Testing lab course.

---

## 1. Installation and Setup

### Prerequisites
- Python 3.10 or newer
- `curl` / `curl.exe`

### Setup Virtual Environment
Clone this repository and create a virtual environment:

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Running Tests

### Run all tests with verbose output:
```powershell
pytest -v
```

### Run tests and generate self-contained HTML report:
```powershell
pytest -v --html=report.html --self-contained-html
```

### Expected Results
- **32 passed, 1 xfailed**
- The single `xfailed` test captures a known backend defect in QuickPizza where excluding all cutting tools returns HTTP 500 instead of HTTP 400.

---

## 3. Input Domain Model for `POST /api/ratings`

This table defines the input space partitioning and **Base Choice Coverage (BCC)** test mapping for creating a rating (`POST /api/ratings`):

| Characteristic | Blocks | Values in the tests | Test Function Covering the Block |
| :--- | :--- | :--- | :--- |
| **C1 Value of stars** | below 1<br>**1 to 5 (base)**<br>above 5 | 0<br>**3**<br>6 | `test_stars_out_of_range[0]`<br>`test_base_choice_is_saved`<br>`test_stars_out_of_range[6]` |
| **C2 Type of stars** | **whole number (base)**<br>decimal<br>text<br>missing | **3**<br>3.5<br>"3"<br>no field | `test_base_choice_is_saved`<br>`test_stars_decimal`<br>`test_stars_text`<br>`test_stars_missing` |
| **C3 Pizza** | **exists (base)**<br>does not exist | **a new pizza**<br>999999999 | `test_base_choice_is_saved`<br>`test_pizza_does_not_exist` |
| **C4 Token** | **the user's own (base)**<br>none<br>wrong length | **from auth**<br>no header<br>token short | `test_base_choice_is_saved`<br>`test_token_missing`<br>`test_token_wrong_length` |

---

## 4. Repository Structure

```text
api-lab/
├── .gitignore               # Standard Python gitignore
├── README.md                # Project documentation and test mapping
├── RESULTS.md               # Lab exercise answers and reflection
├── requirements.txt         # Required Python packages
├── report.html              # Generated HTML test execution report
├── auth.txt                 # Authorization header for curl
├── veg.json                 # Vegetarian pizza request body for curl
├── madeup.txt               # Header with 16-char made-up token
├── conftest.py              # Pytest fixtures and Session management
├── test_names.py            # Step 0.6: Pizza names test
├── test_tools.py            # Step 0.7: Tool listing test with token
├── test_pizza.py            # Step 0.8: Pizza generation & vegetarian check
├── test_users.py            # Step 0.11: New user registration and rating check
├── test_ratings.py          # Step 0.13-0.14: CRUD operations on ratings
├── test_refused.py          # Step 0.15: Negative user authentication cases
├── test_excluded_tools.py   # Step 0.16: Excluded tools & defect hunting (xfail)
├── test_create_rating.py    # Step A1-A2: Base choice coverage for ratings (9 tests)
├── test_update_rating.py    # Step A3: Boundary value testing for rating update
└── test_rating_owner.py     # Step A4: Rating ownership and security tests
```

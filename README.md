# 🧪 Software Testing Lab — Automation QA Project

Automated end-to-end test suite for the **Events & Activities** web application,  
built with **Python + Selenium + pytest** as part of a Software Testing Lab assignment.

---

## 🌐 Live Website

🔗 **[https://events-activities-frontend.vercel.app/](https://events-activities-frontend.vercel.app/)**

---

## 🔐 Test Credentials

| Role  | Email | Password |
|-------|-------|----------|
| Admin | admin@gmail.com | 12345678 |
| Host  | towsif@gmail.com | 12345678 |
| User  | shafee@gmail.com | 12345678 |

---

## 📁 Project Structure

```
qa_project/
 ┣ 📄 config.py                  ← BASE_URL, credentials, screenshot path
 ┣ 📄 utils.py                   ← Screenshot, annotation, bug log, report helpers
 ┣ 📄 conftest.py                ← Shared Chrome driver fixture (pytest auto-loads)
 ┣ 📄 run_all.py                 ← ONE command to run all tests + generate report
 ┣ 📂 tests/
 ┃ ┣ 📄 test_registration.py     ← 8 test cases for Sign Up page
 ┃ ┣ 📄 test_login.py            ← 8 test cases for Login page
 ┃ ┗ 📄 test_dashboard.py        ← 12 test cases for Dashboard page
 ┗ 📂 screenshots/               ← Auto-created; all screenshots saved here
    ┣ 🖼️ CHECKPOINT_*.png         ← Pass checkpoints
    ┣ 🖼️ FAIL_*_ANNOTATED.png     ← Annotated bug screenshots
    ┗ 📄 bug_report.txt           ← Auto-generated bug report
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

> You should see `(venv)` appear at the start of your terminal line — that means it's active.

### 4. Install all required packages
```bash
pip install pytest selenium webdriver-manager
pip install pytest-html
pip install pillow
```

### 5. Install ChromeDriver
Make sure your ChromeDriver version matches your Chrome browser.  
Download from: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

### 6. Configure your test user
Open `config.py` and update before each run:
```python
FULL_NAME     = "Your Test User Name"
EMAIL         = "yourtestuser@gmail.com"
PASSWORD      = "12345678"
CONTACT       = "01800000000"
PROFILE_IMAGE = r"C:\path\to\your\image.jpeg"   # full path to a profile image
```

---

## ▶️ Running the Tests

> ⚠️ Make sure your virtual environment is activated first — you should see `(venv)` in your terminal.

### Run everything with one command:
```bash
python run_all.py
```

### Run all tests with pytest (shows live print output):
```bash
pytest -s tests/
```

### Run a single page only:
```bash
pytest -s tests/test_registration.py
pytest -s tests/test_login.py
pytest -s tests/test_dashboard.py
```

### Run a single test case:
```bash
pytest -s tests/test_dashboard.py::test_welcome_heading_shows_username
```

### Generate an HTML report:
```bash
pytest -s tests/ --html=report.html
```
> Opens `report.html` in your browser — shows full pass/fail details per test case.

---

## 📋 Test Cases

### 📝 Registration Page — `test_registration.py`

| ID | Function | Type | Expected |
|----|----------|------|----------|
| TC-REG-01 | `test_registration_form_loads` | ✅ Pass | All fields visible |
| TC-REG-02 | `test_fill_full_name` | ✅ Pass | Full Name field accepts input |
| TC-REG-03 | `test_fill_email` | ✅ Pass | Email field accepts valid email |
| TC-REG-04 | `test_fill_password` | ✅ Pass | Password fields accept input |
| TC-REG-05 | `test_select_gender` | ✅ Pass | Gender dropdown selects Male |
| TC-REG-06 | `test_upload_profile_image` | ✅ Pass | Image upload input works |
| TC-REG-07 | `test_submit_empty_form` | ❌ Fail Case | Validation errors shown |
| TC-REG-08 | `test_full_registration_flow` | ✅ Pass | Full signup → dashboard redirect |

---

### 🔐 Login Page — `test_login.py`

| ID | Function | Type | Expected |
|----|----------|------|----------|
| TC-LOG-01 | `test_login_form_loads` | ✅ Pass | Email & Password fields visible |
| TC-LOG-02 | `test_fill_login_email` | ✅ Pass | Email field accepts input |
| TC-LOG-03 | `test_fill_login_password` | ✅ Pass | Password field accepts input |
| TC-LOG-04 | `test_login_wrong_password` | ❌ Fail Case | Error message shown |
| TC-LOG-05 | `test_login_empty_fields` | ❌ Fail Case | Validation shown |
| TC-LOG-06 | `test_login_valid_credentials` | ✅ Pass | Success toast appears |
| TC-LOG-07 | `test_login_redirects_to_dashboard` | ✅ Pass | Redirect to /dashboard |
| TC-LOG-08 | `test_logout_flow` | ✅ Pass | Logout toast + redirect to login |

---

### 📊 Dashboard Page — `test_dashboard.py`

| ID | Function | Type | Expected |
|----|----------|------|----------|
| TC-DASH-01 | `test_dashboard_loads` | ✅ Pass | Dashboard URL confirmed |
| TC-DASH-02 | `test_welcome_heading_shows_username` | 🐛 Bug | "Welcome back, Test User 116!" |
| TC-DASH-03 | `test_profile_section_visible` | ✅ Pass | "Your Profile" heading visible |
| TC-DASH-04 | `test_profile_field_full_name` | ✅ Pass | Full Name displays correctly |
| TC-DASH-05 | `test_profile_field_email` | 🐛 Bug | Real email shown, not placeholder |
| TC-DASH-06 | `test_profile_field_contact` | ✅ Pass | Contact number correct |
| TC-DASH-07 | `test_profile_field_gender` | ✅ Pass | Gender shows MALE |
| TC-DASH-08 | `test_account_summary_card` | ✅ Pass | Active, Public, Enabled shown |
| TC-DASH-09 | `test_stat_cards` | ✅ Pass | Status, Role, Member Since correct |
| TC-DASH-10 | `test_sidebar_navigation` | ✅ Pass | All sidebar items present |
| TC-DASH-11 | `test_profile_avatar` | ✅ Pass | Avatar image loads correctly |
| TC-DASH-12 | `test_member_since_and_last_updated` | ✅ Pass | Dates visible |

---

## 📊 Test Summary

| Page | Total | ✅ Pass | ❌ Fail | 🐛 Bugs |
|------|-------|--------|--------|--------|
| Registration | 8 | 7 | 1 | 0 |
| Login | 8 | 6 | 2 | 0 |
| Dashboard | 12 | 10 | 0 | 2 |
| **Total** | **28** | **23** | **3** | **2** |

---

## 🐛 Bugs Found

### BUG-001 — Welcome Back Heading Missing Username

| Field | Detail |
|-------|--------|
| **File** | `tests/test_dashboard.py` → `test_welcome_heading_shows_username` |
| **Location** | Dashboard → Welcome heading |
| **Expected** | `Welcome back, Test User 116!` |
| **Actual** | `Welcome back, !` |
| **Error Type** | `TimeoutException` |
| **Priority** | 🔴 High |

![BUG-001](screenshots/FAIL_Welcome_back_heading_shows_user_s_name_1782545901_ANNOTATED.png)

---

### BUG-002 — Email Address Field Shows Placeholder Text

| Field | Detail |
|-------|--------|
| **File** | `tests/test_dashboard.py` → `test_profile_field_email` |
| **Location** | Dashboard → Your Profile → Email Address |
| **Expected** | `testuser116@gmail.com` |
| **Actual** | `userInfo.email` |
| **Error Type** | `AssertionError` |
| **Priority** | 🔴 High |

![BUG-002](screenshots/FAIL_Profile_field_-_Email_Address_1782545902_ANNOTATED.png)

---

## 🔍 How Bug Screenshots Work

Every failing test automatically:

1. Takes a raw screenshot of the current browser state
2. Draws a **red box** around the broken element
3. Adds a **red arrow** pointing to the issue
4. Adds a **yellow label** describing what went wrong
5. Saves the annotated image to `screenshots/FAIL_*_ANNOTATED.png`
6. Logs the bug to `screenshots/bug_report.txt`

All of this happens via `utils.py` → `annotate_failure()` — no manual work needed.

---

## 📄 Auto-Generated Bug Report

After every run, `screenshots/bug_report.txt` is created automatically:

```
2 bug(s) found during this run:

1. Step      : Welcome back heading shows user's name
   Reason    : User's name is missing from the 'Welcome back' heading (TimeoutException)
   Screenshot: screenshots\FAIL_Welcome_back_heading_..._ANNOTATED.png

2. Step      : Profile field - Email Address
   Reason    : Email Address field shows placeholder/wrong text instead of the real email
   Screenshot: screenshots\FAIL_Profile_field_-_Email_Address_..._ANNOTATED.png
```

---


---

## 🤖 ClickUp Bug Report Prompt

After each test run, use this prompt with any AI tool to instantly generate  
professional ClickUp task content — no manual writing needed.

### How to use it:
1. Copy the prompt below
2. Paste it into Claude, ChatGPT, or any AI tool
3. Give it your page name, test results, and bug details
4. Paste the output directly into ClickUp

### The Prompt:

```
You are a QA bug report assistant. Your job is to generate
professional ClickUp task content for any webpage test result.

INPUTS YOU WILL RECEIVE:
- Page name (e.g. Dashboard, Login, Sign Up)
- Test results (passed checks + failed checks)
- Bug details (what was expected vs actual, error type)
- Screenshot file names (if any)

YOUR BEHAVIOR RULES:

1. NEVER create a bug task for a page that has zero bugs.
   - If all checks passed → generate a QA Report task (status: DONE)
   - If any check failed → generate a Bug Report task (status: TO DO)

2. FOR PASSED PAGES, generate this format:
---
Task Name: QA Report — [Page Name] Page
Tags: [relevant tags]
Status: DEV DONE
Priority: Normal

Steps:
[list the fields/elements that were tested]

Steps to Reproduce:
[how to reach this page]

Actual Result:
✅ [each passed check on its own line]
Bugs Found: None
---

3. FOR FAILED PAGES, generate this format:
---
Task Name: BUG Report — [Page Name] Page
Tags: bug, [page name], ui
Status: TO DO
Priority: High

Steps:
[list all elements tested on this page]

Steps to Reproduce:
[how to reach this page]

Actual Result:
❌ [number] bugs found — see subtasks

━━━━━━━━━━━━━━━━━━━━
SUBTASK FOR EACH BUG:
━━━━━━━━━━━━━━━━━━━━
Subtask Name: BUG-[number]: [short bug title]
Priority: High
Expected: [what should have appeared]
Actual: [what actually appeared]
Error: [error type if known e.g. TimeoutException, AssertionError]
Screenshot: [filename if provided]
---

4. STRUCTURE RULES:
- One main task per page
- One subtask per individual bug
- Never merge two bugs into one subtask
- Always attach annotated screenshots to the relevant subtask, not the main task

5. TONE:
- Professional, concise
- No filler words
- Facts only — expected vs actual, nothing else
```

### Example input you give the AI:
```
Page: Dashboard
Passed: Dashboard loads, Profile section visible, Stat cards correct
Failed:
  - Welcome heading shows "Welcome back, !" instead of "Welcome back, Test User 116!"
    Error: TimeoutException
    Screenshot: FAIL_Welcome_back_heading_ANNOTATED.png

  - Email field shows "userInfo.email" instead of "testuser116@gmail.com"
    Error: AssertionError
    Screenshot: FAIL_Profile_field_Email_Address_ANNOTATED.png
```

### Example output the AI generates:
```
Task Name: BUG Report — Dashboard Page
Tags: bug, dashboard, ui
Status: TO DO
Priority: High

Steps:
1. Welcome back heading with user's name
2. Profile section (Full Name, Email, Contact, Gender, Address)
3. Account Summary sidebar
4. Stat cards (Account Status, Role Permissions, Member Since)

Steps to Reproduce:
1. Visit the website (event management system)
2. Login with valid credentials
3. Get redirected to the dashboard

Actual Result:
❌ 2 bugs found — see subtasks

━━━━━━━━━━━━━━━━━━━━
SUBTASK FOR EACH BUG:
━━━━━━━━━━━━━━━━━━━━
Subtask Name: BUG-001: Welcome Back Heading Missing Username
Priority: High
Expected: "Welcome back, Test User 116!"
Actual: "Welcome back, !"
Error: TimeoutException
Screenshot: FAIL_Welcome_back_heading_ANNOTATED.png

Subtask Name: BUG-002: Email Address Field Shows Placeholder Text
Priority: High
Expected: testuser116@gmail.com
Actual: userInfo.email
Error: AssertionError
Screenshot: FAIL_Profile_field_Email_Address_ANNOTATED.png
```

> 💡 This prompt works for **any website and any page** — not just this project.  
> Feed it your test results and it handles the ClickUp formatting automatically.

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x | Test scripting language |
| Selenium | 4.x | Browser automation |
| pytest | 7.x | Test runner & reporting |
| Pillow | 10.x | Screenshot annotation |
| ChromeDriver | Match Chrome | Browser driver |

---

## 👤 Author

**MD Irfanul Kabir Hira**  
Software Testing Lab Assignment  
📅 Date: June 2026

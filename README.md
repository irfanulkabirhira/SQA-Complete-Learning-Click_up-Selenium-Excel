# 🧪 QA Bug Report — Events & Activities Web App

Automated QA test report for the **Events & Activities** event management web application.  
This report covers end-to-end testing of the **Sign Up**, **Login**, and **Dashboard** pages.

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

## 📋 Test Summary

| Page | Total Cases | Passed | Failed | Result |
|------|-------------|--------|--------|--------|
| Sign Up | 3 | 3 | 0 | ✅ PASS |
| Login | 4 | 4 | 0 | ✅ PASS |
| Dashboard | 7 | 5 | 2 | ❌ FAIL |
| **Total** | **14** | **12** | **2** | **❌ 2 Bugs Found** |

---

## ✅ Sign Up Page — PASSED

**Steps Tested:**
- Registration form loads with all required fields
- User can register with valid credentials (Full Name, Email, Password, Confirm Password)
- Successful redirect to dashboard after signup

**Result:** All 3 test cases passed. No bugs found.

---

## ✅ Login Page — PASSED

**Steps Tested:**
- Login form loads with Email & Password fields
- User can login with valid credentials
- Success toast: *"You have been logged in successfully"* appears
- Logout flow works correctly with confirmation toast

**Result:** All 4 test cases passed. No bugs found.

---

## ❌ Dashboard Page — 2 BUGS FOUND

**Steps Tested:**
- Dashboard loads after login
- Sidebar navigation renders correctly
- Profile section displays correct user data
- Account Summary sidebar loads
- Stat cards display correctly
- Welcome back heading shows user's name ❌
- Profile Email Address field shows real email ❌

---

### 🐛 BUG-001 — Welcome Back Heading Missing Username

| Field | Detail |
|-------|--------|
| **Location** | Dashboard → Welcome heading |
| **Expected** | `Welcome back, Test User 116!` |
| **Actual** | `Welcome back, !` |
| **Error Type** | `TimeoutException` |
| **Priority** | 🔴 High |
| **Status** | Open |

**Screenshot:**

![BUG-001](screenshots/FAIL_Welcome_back_heading_shows_user_s_name_1782545901_ANNOTATED.png)

---

### 🐛 BUG-002 — Email Address Field Shows Placeholder Text

| Field | Detail |
|-------|--------|
| **Location** | Dashboard → Your Profile → Email Address |
| **Expected** | `testuser116@gmail.com` |
| **Actual** | `userInfo.email` |
| **Error Type** | `AssertionError` |
| **Priority** | 🔴 High |
| **Status** | Open |

**Screenshot:**

![BUG-002](screenshots/FAIL_Profile_field_-_Email_Address_1782545902_ANNOTATED.png)

---

## 📁 Project Structure

```
📦 qa-bug-report
 ┣ 📂 screenshots
 ┃ ┣ 🖼️ CHECKPOINT_step1_signup_dashboard.png
 ┃ ┣ 🖼️ CHECKPOINT_step2_logout.png
 ┃ ┣ 🖼️ CHECKPOINT_step3_login_dashboard.png
 ┃ ┣ 🖼️ CHECKPOINT_step4_profile_fields.png
 ┃ ┣ 🖼️ CHECKPOINT_step4_stat_cards.png
 ┃ ┣ 🖼️ CHECKPOINT_step4_account_summary.png
 ┃ ┣ 🖼️ CHECKPOINT_step4_avatar.png
 ┃ ┣ 🖼️ CHECKPOINT_step4_sidebar.png
 ┃ ┣ 🖼️ CHECKPOINT_full_flow_complete.png
 ┃ ┣ 🖼️ FAIL_Welcome_back_heading_shows_user_s_name_ANNOTATED.png
 ┃ ┗ 🖼️ FAIL_Profile_field_-_Email_Address_ANNOTATED.png
 ┣ 📊 QA_Test_Report.xlsx
 ┣ 📄 bug_report.txt
 ┗ 📄 README.md
```

---

## 🤖 ClickUp Bug Report Prompt (Reusable)

This project uses a reusable AI prompt to generate ClickUp task content for any webpage test.  
The prompt handles:
- ✅ Passed pages → QA Report task (status: DEV DONE)
- ❌ Failed pages → Bug Report task + subtasks per bug (status: TO DO)

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
   Task Name: QA Report — [Page Name] Page
   Tags: [relevant tags]
   Status: DEV DONE
   Priority: Normal
   Steps: [list the fields/elements that were tested]
   Steps to Reproduce: [how to reach this page]
   Actual Result: ✅ [each passed check on its own line]
   Bugs Found: None

3. FOR FAILED PAGES, generate this format:
   Task Name: BUG Report — [Page Name] Page
   Tags: bug, [page name], ui
   Status: TO DO
   Priority: High
   Steps: [list all elements tested on this page]
   Steps to Reproduce: [how to reach this page]
   Actual Result: ❌ [number] bugs found — see subtasks

   SUBTASK FOR EACH BUG:
   Subtask Name: BUG-[number]: [short bug title]
   Priority: High
   Expected: [what should have appeared]
   Actual: [what actually appeared]
   Error: [error type if known]
   Screenshot: [filename if provided]

4. STRUCTURE RULES:
   - One main task per page
   - One subtask per individual bug
   - Never merge two bugs into one subtask
   - Always attach annotated screenshots to the relevant subtask

5. TONE: Professional, concise, facts only.
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| Python + Selenium | Automated test execution |
| ClickUp | Bug tracking & task management |
| Microsoft Excel | QA test report spreadsheet |
| Claude AI | Bug report generation & prompt engineering |
| GitHub | Project documentation |

---

## 👤 Author

**MD Irfanul Kabir Hira**  
QA Tester  
📅 Test Run Date: June 27, 2026

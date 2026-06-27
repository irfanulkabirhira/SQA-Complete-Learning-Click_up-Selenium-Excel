import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Pillow for annotating failure screenshots
try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False

BASE_URL = "https://events-activities-frontend.vercel.app"

# ─── Edit these before each run ───────────────────────────────────────────────
FULL_NAME     = "Test User 116"
EMAIL         = "testuser116@gmail.com"
PASSWORD      = "12345678"
CONTACT       = "01823456799"
PROFILE_IMAGE = r"D:\pic.jpeg"
# ──────────────────────────────────────────────────────────────────────────────

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Every bug found during the run gets appended here as a dict:
# {"step": str, "reason": str, "screenshot": str}
BUG_LOG = []


# ══════════════════════════════════════════════════════════════════════════════
#  SCREENSHOT + ANNOTATION HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def safe_filename(name):
    """
    Strip / replace characters that are illegal in Windows filenames.
    Illegal chars: \\ / : * ? " < > |
    We replace them with '-' so the name stays readable.
    """
    for ch in r'\/:*?"<>|':
        name = name.replace(ch, "-")
    return name


def take_screenshot(driver, name):
    filename = os.path.join(SCREENSHOT_DIR, f"{safe_filename(name)}_{int(time.time())}.png")
    driver.save_screenshot(filename)
    print(f"\n📸 Screenshot saved: {filename}")
    return filename


# Maps a *substring* of the step name -> a Selenium locator used to find the
# broken element so we can draw the red box + arrow around it.
HINT_MAP = [
    ("Full Name",        (By.ID, "name")),
    ("Address",          (By.ID, "address")),
    ("Email Address",    (By.XPATH, "//*[contains(text(),'Email Address')]/following::*[1]")),
    ("Login Email",      (By.ID, "email")),
    ("Email",             (By.ID, "email")),
    ("Contact Number",   (By.ID, "contactNumber")),
    ("About",            (By.ID, "about")),
    ("Interests",        (By.ID, "interests")),
    ("Login Password",   (By.ID, "password")),
    ("Confirm Password", (By.ID, "confirmPassword")),
    ("Password",         (By.ID, "password")),
    ("gender dropdown",  (By.XPATH, "//button[@role='combobox']")),
    ("Select Male",      (By.XPATH, "//button[@role='combobox']")),
    ("profile image",    (By.XPATH, "//input[@type='file']")),
    ("Create Account",   (By.XPATH, "//button[normalize-space()='Create Account']")),
    ("user menu",        (By.XPATH, "//button[@aria-haspopup='menu']")),
    ("Logout",           (By.XPATH, "//button[normalize-space()='Logout']")),
    ("login submit",     (By.XPATH, "//button[@type='submit']")),
    ("Your Profile",     (By.XPATH, "//*[contains(text(),'Your Profile')]")),
    ("Welcome back",     (By.XPATH, "//*[contains(text(),'Welcome back')]")),
    ("Account Summary",  (By.XPATH, "//*[contains(text(),'Account Summary')]")),
    ("Member since",     (By.XPATH, "//*[contains(text(),'Member since') or contains(text(),'member since')]")),
    ("Last Updated",     (By.XPATH, "//*[contains(text(),'Last Updated')]")),
]


def _guess_element(driver, step_name):
    """Best-effort lookup of the element related to a failing step."""
    step_lower = step_name.lower()
    best_hint = None
    best_locator = None
    for hint, locator in HINT_MAP:
        if hint.lower() in step_lower:
            if best_hint is None or len(hint) > len(best_hint):
                best_hint = hint
                best_locator = locator
    if best_locator is None:
        return None
    try:
        return driver.find_element(*best_locator)
    except Exception:
        return None


def annotate_failure(driver, step_name, element=None, reason="Element not interactable"):
    """
    Take a screenshot and draw on it:
      • A red highlight box around the broken element (if found)
      • A red arrow pointing to it
      • A red label banner at the top describing the bug
    Returns the annotated file path.
    """
    raw_path = take_screenshot(driver, f"FAIL_{step_name.replace(' ', '_')}")

    if not PILLOW_OK:
        print("⚠ Pillow not installed — saving plain screenshot only. "
              "Run: pip install pillow")
        return raw_path

    try:
        img  = Image.open(raw_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        W, H = img.size

        try:
            font_big   = ImageFont.truetype("arial.ttf", 28)
            font_small = ImageFont.truetype("arial.ttf", 22)
        except Exception:
            font_big   = ImageFont.load_default()
            font_small = ImageFont.load_default()

        RED    = (220, 38, 38)
        WHITE  = (255, 255, 255)
        YELLOW = (253, 224, 71)

        # Top banner
        banner_h = 54
        draw.rectangle([0, 0, W, banner_h], fill=RED)
        draw.text((12, 12), f"BUG: {step_name}", fill=WHITE, font=font_big)

        target_element = element or _guess_element(driver, step_name)

        if target_element:
            try:
                loc  = target_element.location
                size = target_element.size
                x1   = int(loc["x"])
                y1   = int(loc["y"]) + banner_h
                x2   = x1 + int(size["width"])
                y2   = y1 + int(size["height"])

                for t in range(4):
                    draw.rectangle([x1 - t, y1 - t, x2 + t, y2 + t], outline=RED)

                ax_end, ay_end = x2 + 10, (y1 + y2) // 2
                ax_start       = min(ax_end + 120, W - 20)
                ay_start       = ay_end

                draw.line([(ax_start, ay_start), (ax_end, ay_end)],
                          fill=RED, width=5)
                draw.polygon([
                    (ax_end,      ay_end),
                    (ax_end + 18, ay_end - 12),
                    (ax_end + 18, ay_end + 12),
                ], fill=RED)

                label = f"! {reason}"
                lx, ly = ax_start + 6, ay_start - 16
                label_w = max(280, 11 * len(label))
                draw.rectangle([lx - 4, ly - 4, lx + label_w, ly + 30],
                                fill=YELLOW, outline=RED, width=2)
                draw.text((lx, ly), label, fill=(60, 0, 0), font=font_small)

            except Exception as box_err:
                print(f"(could not draw box/arrow for '{step_name}': {box_err})")

        else:
            note_label = f"! {reason} (element not located on page)"
            draw.rectangle([20, banner_h + 20, 20 + max(320, 11 * len(note_label)), banner_h + 60],
                            fill=YELLOW, outline=RED, width=2)
            draw.text((28, banner_h + 28), note_label, fill=(60, 0, 0), font=font_small)

        note = "Use this screenshot for your bug report"
        draw.rectangle([0, H - 38, W, H], fill=(30, 30, 30))
        draw.text((12, H - 30), note, fill=(200, 200, 200), font=font_small)

        annotated_path = raw_path.replace(".png", "_ANNOTATED.png")
        img.save(annotated_path)
        print(f"🔴 Annotated screenshot: {annotated_path}")
        return annotated_path

    except Exception as ex:
        print(f"Annotation failed ({ex}), plain screenshot kept: {raw_path}")
        return raw_path


# ══════════════════════════════════════════════════════════════════════════════
#  SAFE ACTION  +  FILL FIELD
# ══════════════════════════════════════════════════════════════════════════════

def safe_action(driver, action_fn, step_name, element=None, bug_hint=None):
    """
    Runs action_fn(). On failure: annotates screenshot, logs bug, prints error,
    and returns None so the test keeps running.
    """
    try:
        return action_fn()
    except Exception as e:
        exc_summary = f"{type(e).__name__}: {e}".splitlines()[0]
        reason = f"{bug_hint} ({type(e).__name__})" if bug_hint else exc_summary
        annotated = annotate_failure(
            driver, step_name, element=element,
            reason=(bug_hint or type(e).__name__)
        )
        BUG_LOG.append({
            "step": step_name,
            "reason": reason,
            "screenshot": annotated,
        })
        print(f"\n❌ FAILED at: '{step_name}'")
        print(f"   Reason   : {reason}")
        print(f"   Detail   : {exc_summary}")
        print(f"   Screenshot: {annotated}")
        print("   ↳ Continuing to next step...\n")
        return None


def find_any(driver, xpaths, timeout=10):
    wait = WebDriverWait(driver, timeout)
    for xp in xpaths:
        try:
            el = wait.until(EC.visibility_of_element_located((By.XPATH, xp)))
            if el.is_displayed():
                return el
        except Exception:
            continue
    raise AssertionError(
        "None of these XPaths found a visible element:\n" + "\n".join(xpaths)
    )


def fill_field(driver, wait, by, locator, value, label):
    """Wait until clickable, scroll into view, click, clear, type."""
    def _fill():
        el = wait.until(EC.element_to_be_clickable((by, locator)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.3)
        el.click()
        el.clear()
        el.send_keys(value)
    safe_action(driver, _fill, f"Fill {label}")


# ── Fixture ───────────────────────────────────────────────────────────────────
@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


# ══════════════════════════════════════════════════════════════════════════════
#  FULL FLOW  →  Sign Up  →  Logout  →  Login  →  Dashboard
# ══════════════════════════════════════════════════════════════════════════════
def test_full_flow(driver):
    wait = WebDriverWait(driver, 25)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 1 — SIGN UP
    # ──────────────────────────────────────────────────────────────────────────
    print("\n========== STEP 1: SIGN UP ==========")

    safe_action(driver, lambda: driver.get(f"{BASE_URL}/register"), "Open register page")
    safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located((By.ID, "name"))),
        "Register page visible")
    time.sleep(2)

    fill_field(driver, wait, By.ID, "name",          FULL_NAME,           "Full Name")
    fill_field(driver, wait, By.ID, "address",       "Test Address",      "Address")
    fill_field(driver, wait, By.ID, "email",         EMAIL,               "Email")
    fill_field(driver, wait, By.ID, "contactNumber", CONTACT,             "Contact Number")
    fill_field(driver, wait, By.ID, "about",         "Test About",        "About")
    fill_field(driver, wait, By.ID, "interests",     "Testing, Selenium", "Interests")

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox']"))
        ).click(),
        "Open gender dropdown")
    time.sleep(1)

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='option' and contains(., 'Male')]")
            )
        ).click(),
        "Select Male gender")

    fill_field(driver, wait, By.ID, "password",        PASSWORD, "Password")
    fill_field(driver, wait, By.ID, "confirmPassword", PASSWORD, "Confirm Password")

    safe_action(driver,
        lambda: driver.find_element(
            By.XPATH, "//input[@type='file']"
        ).send_keys(PROFILE_IMAGE),
        "Upload profile image")
    time.sleep(4)

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Create Account']")
            )
        ).click(),
        "Click Create Account button")

    time.sleep(8)
    safe_action(driver,
        lambda: wait.until(EC.url_contains("/dashboard")),
        "Redirect to dashboard after signup")

    take_screenshot(driver, "CHECKPOINT_step1_signup_dashboard")
    print("Signup flow attempted (see above for any failures)")
    time.sleep(3)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 2 — LOGOUT
    # ──────────────────────────────────────────────────────────────────────────
    print("\n========== STEP 2: LOGOUT AFTER SIGNUP ==========")

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-haspopup='menu']"))
        ).click(),
        "Click user menu button")
    time.sleep(1)

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Logout']"))
        ).click(),
        "Click Logout button")
    time.sleep(3)

    def check_logout_toast():
        toast = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'logged out') or contains(text(),'success')]")
        ))
        assert "logged" in toast.text.lower() or "success" in toast.text.lower()
        print("Logout toast:", toast.text)

    safe_action(driver, check_logout_toast, "Logout toast message")
    safe_action(driver,
        lambda: wait.until(EC.url_contains("/login")),
        "Redirect to login after logout")

    take_screenshot(driver, "CHECKPOINT_step2_logout")
    print("Logout flow attempted (see above for any failures)")
    time.sleep(2)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 3 — LOGIN
    # ──────────────────────────────────────────────────────────────────────────
    print("\n========== STEP 3: LOGIN ==========")

    safe_action(driver, lambda: driver.get(f"{BASE_URL}/login"), "Open login page")
    safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located((By.ID, "email"))),
        "Login page visible")
    time.sleep(2)

    fill_field(driver, wait, By.ID, "email",    EMAIL,    "Login Email")
    fill_field(driver, wait, By.ID, "password", PASSWORD, "Login Password")

    safe_action(driver,
        lambda: wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click(),
        "Click login submit button")

    def check_login_toast():
        toast = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'logged in') or contains(text(),'success')]")
        ))
        assert (
            "success" in toast.text.lower()
            or "login"  in toast.text.lower()
            or "logged" in toast.text.lower()
        )
        print("Login toast:", toast.text)

    safe_action(driver, check_login_toast, "Login toast message")
    safe_action(driver,
        lambda: wait.until(EC.url_contains("/dashboard")),
        "Redirect to dashboard after login")

    take_screenshot(driver, "CHECKPOINT_step3_login_dashboard")
    print("Login flow attempted (see above for any failures)")
    time.sleep(3)

    # ──────────────────────────────────────────────────────────────────────────
    # STEP 4 — DASHBOARD CHECKS
    # ──────────────────────────────────────────────────────────────────────────
    print("\n========== STEP 4: DASHBOARD VERIFICATION ==========")

    safe_action(driver,
        lambda: (_ for _ in ()).throw(AssertionError(f"Wrong URL: {driver.current_url}"))
                if "/dashboard" not in driver.current_url else None,
        "Dashboard URL check")
    print("Dashboard URL checked")

    # ── FIX 1: colon removed from step name ──────────────────────────────────
    safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(text(),'Welcome back') and contains(text(),'{FULL_NAME}')]")
        )),
        "Welcome back heading shows user's name",
        bug_hint="User's name is missing from the 'Welcome back' heading")
    print("'Welcome back' heading checked")

    safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Your Profile')]")
        )),
        "Your Profile heading")
    print("'Your Profile' heading checked")

    # ── FIX 2: step names now use " - " instead of ": " ─────────────────────
    profile_checks = {
        "Full Name":      f"//*[contains(text(),'{FULL_NAME}')]",
        "Contact Number": f"//*[contains(text(),'{CONTACT}')]",
        "Address":        "//*[contains(text(),'Test Address')]",
        "Gender":         "//*[contains(text(),'MALE') or contains(text(),'Male')]",
    }
    for field_name, xp in profile_checks.items():
        result = safe_action(driver,
            lambda xp=xp: wait.until(EC.visibility_of_element_located((By.XPATH, xp))),
            f"Profile field - {field_name}")          # <-- was "Profile field: {field_name}"
        print(f"  Profile field '{field_name}' {'✓' if result else '✗ (logged as bug)'}")

    def check_email_field():
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Email Address')]")
        ))
        value_el = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Email Address')]/following::*[1]"
        )
        actual_text = value_el.text.strip()
        assert actual_text == EMAIL, (
            f"Email Address field shows '{actual_text}' instead of '{EMAIL}'"
        )
        return value_el

    # ── FIX 3: step name uses " - " instead of ": " ──────────────────────────
    email_result = safe_action(
        driver, check_email_field, "Profile field - Email Address",   # <-- was "Profile field: Email Address"
        bug_hint="Email Address field shows placeholder/wrong text instead of the real email"
    )
    print(f"  Profile field 'Email Address' {'✓' if email_result else '✗ (logged as bug)'}")

    take_screenshot(driver, "CHECKPOINT_step4_profile_fields")

    safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Account Summary')]")
        )),
        "Account Summary card")
    print("Account Summary card checked")

    for value in ["Active", "Public", "Enabled"]:
        result = safe_action(driver,
            lambda v=value: wait.until(EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{v}')]")
            )),
            f"Account Summary value - {value}")       # <-- was "Account Summary value: {value}"
        print(f"  Account Summary '{value}' {'✓' if result else '✗ (logged as bug)'}")

    take_screenshot(driver, "CHECKPOINT_step4_account_summary")

    stat_checks = [
        ("Account Status",   "Active"),
        ("Role Permissions", "USER"),
        ("Member Since",     "2026"),
    ]
    for label, value in stat_checks:
        def check_stat(label=label, value=value):
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{label}')]")
            ))
            el = driver.find_element(
                By.XPATH,
                f"//*[contains(text(),'{label}')]/following::*[contains(text(),'{value}')][1]"
            )
            assert el.is_displayed()
            return True
        # ── FIX 4: step name uses " - " instead of ": " and "->" instead of "→" ──
        result = safe_action(driver, check_stat, f"Stat card - {label} - {value}")
        print(f"  Stat card '{label}' -> '{value}' {'✓' if result else '✗ (logged as bug)'}")

    take_screenshot(driver, "CHECKPOINT_step4_stat_cards")

    sidebar_checks = {
        "Back to Home": [
            "//a[contains(text(),'Back to Home')]",
            "//span[contains(text(),'Back to Home')]",
            "//*[normalize-space(text())='Back to Home']",
            "//*[contains(.,'Back to Home') and not(*[contains(.,'Back to Home')])]",
            "//*[contains(normalize-space(),'Back to Home')]",
        ],
        "Dashboard":       ["//a[contains(text(),'Dashboard')]",
                            "//span[contains(text(),'Dashboard')]",
                            "//*[normalize-space(text())='Dashboard']"],
        "My Profile":      ["//a[contains(text(),'My Profile')]",
                            "//span[contains(text(),'My Profile')]",
                            "//*[normalize-space(text())='My Profile']"],
        "Change Password": ["//a[contains(text(),'Change Password')]",
                            "//span[contains(text(),'Change Password')]",
                            "//*[normalize-space(text())='Change Password']"],
        "My Events":       ["//a[contains(text(),'My Events')]",
                            "//span[contains(text(),'My Events')]",
                            "//*[normalize-space(text())='My Events']"],
        "My Applications": ["//a[contains(text(),'My Applications')]",
                            "//span[contains(text(),'My Applications')]",
                            "//*[normalize-space(text())='My Applications']"],
    }
    for item_name, xpaths in sidebar_checks.items():
        result = safe_action(driver,
            lambda xps=xpaths: find_any(driver, xps, timeout=10),
            f"Sidebar item - {item_name}")            # <-- was "Sidebar item: {item_name}"
        print(f"  Sidebar '{item_name}' {'✓' if result else '✗ (logged as bug)'}")

    take_screenshot(driver, "CHECKPOINT_step4_sidebar")

    member_el = safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located(
            (By.XPATH,
             "//*[contains(text(),'Member since') or contains(text(),'member since')]")
        )),
        "Member since text")
    if member_el:
        print(f"Member since: '{member_el.text}' ✓")
    else:
        print("Member since text — logged as bug")

    last_updated = safe_action(driver,
        lambda: wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Last Updated')]")
        )),
        "Last Updated field")
    print(f"Last Updated {'✓' if last_updated else '— logged as bug'}")

    def check_avatar():
        avatar = driver.find_element(By.XPATH, "//img")
        natural_width = driver.execute_script("return arguments[0].naturalWidth;", avatar)
        assert natural_width > 0, "Avatar broken (naturalWidth is 0)"
        return natural_width

    avatar_width = safe_action(driver, check_avatar, "Profile avatar image")
    if avatar_width:
        take_screenshot(driver, "CHECKPOINT_step4_avatar")
        print(f"Profile avatar loaded ✓  (naturalWidth: {avatar_width}px)")
    else:
        print("Profile avatar — logged as bug")

    take_screenshot(driver, "CHECKPOINT_full_flow_complete")

    # ──────────────────────────────────────────────────────────────────────────
    # FINAL BUG REPORT
    # ──────────────────────────────────────────────────────────────────────────
    print("\n========== FULL FLOW COMPLETE — BUG REPORT ==========")

    report_path = os.path.join(SCREENSHOT_DIR, "bug_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        if not BUG_LOG:
            msg = "No bugs found. All steps passed."
            print(msg)
            f.write(msg + "\n")
        else:
            header = f"{len(BUG_LOG)} bug(s) found during this run:\n"
            print(header)
            f.write(header + "\n")
            for i, bug in enumerate(BUG_LOG, start=1):
                entry = (
                    f"{i}. Step      : {bug['step']}\n"
                    f"   Reason    : {bug['reason']}\n"
                    f"   Screenshot: {bug['screenshot']}\n"
                )
                print(entry)
                f.write(entry + "\n")

    print(f"Full bug report saved to: {report_path}")
    print("========================================================\n")
    time.sleep(2)
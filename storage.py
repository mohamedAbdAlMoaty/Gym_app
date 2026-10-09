import calendar
import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATE_FORMAT = "%Y-%m-%d"

PLANS = {
    "Monthly": {"months": 1, "price": 50.0},
    "3 Months": {"months": 3, "price": 120.0},
    "6 Months": {"months": 6, "price": 250.0},
}
PAYMENT_METHODS = ["Cash", "Card", "Bank Transfer"]


# =========================
# FILE ACCESS
# =========================

def _path(name):
    return DATA_DIR / f"{name}.json"


def load(name):
    """Return the list stored in data/<name>.json ([] if missing/empty)."""
    path = _path(name)
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        data = json.loads(text)
    except json.JSONDecodeError:
        # Keep the broken file instead of silently overwriting it later.
        path.replace(path.with_suffix(".corrupt.json"))
        return []
    return data if isinstance(data, list) else []


def save(name, items):
    DATA_DIR.mkdir(exist_ok=True)
    tmp = _path(name).with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    tmp.replace(_path(name))  # atomic: never leaves a half-written file


def next_id(name, key, prefix, width=3):
    highest = 0
    for item in load(name):
        value = str(item.get(key, ""))
        if value.startswith(prefix) and value[len(prefix):].isdigit():
            highest = max(highest, int(value[len(prefix):]))
    return f"{prefix}{highest + 1:0{width}d}"


# =========================
# DATES / FORMATTING
# =========================

def today_str():
    return date.today().strftime(DATE_FORMAT)


def parse_date(text):
    """Return a date, or None if text is not YYYY-MM-DD."""
    try:
        return datetime.strptime(text.strip(), DATE_FORMAT).date()
    except (ValueError, AttributeError):
        return None


def parse_time(text):
    """Return 'HH:MM' (normalised), or None if invalid."""
    try:
        return datetime.strptime(text.strip(), "%H:%M").strftime("%H:%M")
    except (ValueError, AttributeError):
        return None


def add_months(d, months):
    index = d.month - 1 + months
    year, month = d.year + index // 12, index % 12 + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def money(amount):
    return f"€{float(amount):,.2f}"


# =========================
# LOOKUPS
# =========================

def get_member(member_id):
    return next((m for m in load("members") if m["member_id"] == member_id), None)


def member_name(member_id):
    member = get_member(member_id)
    return member["name"] if member else member_id


def get_trainer(trainer_id):
    return next((t for t in load("trainers") if t["trainer_id"] == trainer_id), None)


def trainer_name(trainer_id):
    trainer = get_trainer(trainer_id)
    return trainer["name"] if trainer else "Unassigned"


# =========================
# MEMBERSHIPS
# =========================

def membership_status(membership):
    end = parse_date(membership["end_date"])
    return "Active" if end and end >= date.today() else "Expired"


def member_memberships(member_id, memberships=None):
    memberships = load("memberships") if memberships is None else memberships
    return [m for m in memberships if m["member_id"] == member_id]


def latest_membership(member_id, memberships=None):
    owned = member_memberships(member_id, memberships)
    return max(owned, key=lambda m: m["end_date"]) if owned else None


def member_status(member_id, memberships=None):
    """'Active' if any membership is still valid, 'Expired' if all ended, else 'No Membership'."""
    owned = member_memberships(member_id, memberships)
    if not owned:
        return "No Membership"
    return "Active" if any(membership_status(m) == "Active" for m in owned) else "Expired"


def renewal_start(member_id):
    """Day after the current membership ends, or today if it already ended / none exists."""
    latest = latest_membership(member_id)
    if latest:
        end = parse_date(latest["end_date"])
        if end and end >= date.today():
            return end + timedelta(days=1)
    return date.today()


def create_membership(member_id, plan, start, method, amount=None):
    """Create a membership AND its payment. Used for both new memberships and renewals."""
    end = add_months(start, PLANS[plan]["months"]) - timedelta(days=1)
    amount = PLANS[plan]["price"] if amount is None else amount

    membership = {
        "membership_id": next_id("memberships", "membership_id", "MS"),
        "member_id": member_id,
        "plan": plan,
        "start_date": start.strftime(DATE_FORMAT),
        "end_date": end.strftime(DATE_FORMAT),
    }
    memberships = load("memberships")
    memberships.append(membership)
    save("memberships", memberships)

    payment = add_payment(member_id, membership["membership_id"], amount, start.strftime(DATE_FORMAT), method)
    return membership, payment


# =========================
# PAYMENTS
# =========================

def add_payment(member_id, membership_id, amount, payment_date, method):
    payment = {
        "payment_id": next_id("payments", "payment_id", "P"),
        "member_id": member_id,
        "membership_id": membership_id,
        "amount": float(amount),
        "payment_date": payment_date,
        "payment_method": method,
    }
    payments = load("payments")
    payments.append(payment)
    save("payments", payments)
    return payment


# =========================
# ATTENDANCE
# =========================

def open_attendance(member_id):
    """The member's attendance record that has no check-out yet, if any."""
    return next((a for a in load("attendance")
                 if a["member_id"] == member_id and not a.get("check_out")), None)


def add_attendance(member_id, day, check_in):
    record = {
        "attendance_id": next_id("attendance", "attendance_id", "A"),
        "member_id": member_id,
        "date": day,
        "check_in": check_in,
        "check_out": "",
    }
    records = load("attendance")
    records.append(record)
    save("attendance", records)
    return record

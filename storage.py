import calendar
import json

from datetime import date, datetime, timedelta
from pathlib import Path

from models.payment import Payment
from models.membership import Membership


# =========================
# CONFIGURATION
# =========================

DATA_DIR = Path(__file__).resolve().parent / "data"

DATE_FORMAT = "%Y-%m-%d"


PLANS = {
    "Monthly": {
        "months": 1,
        "price": 50.0,
    },
    "3 Months": {
        "months": 3,
        "price": 120.0,
    },
    "6 Months": {
        "months": 6,
        "price": 250.0,
    },
}


PAYMENT_METHODS = list(Payment.ALLOWED_METHODS)


# =========================
# FILE ACCESS
# =========================


def _path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


def load(name: str) -> list:
    """
    Load data from data/<name>.json.

    Returns an empty list if:
    - the file does not exist
    - the file is empty
    """

    path = _path(name)

    if not path.exists():
        return []

    try:
        text = path.read_text(encoding="utf-8").strip()

        if not text:
            return []

        data = json.loads(text)

    except json.JSONDecodeError:
        corrupt_path = path.with_suffix(".corrupt.json")

        path.replace(corrupt_path)

        return []

    return data if isinstance(data, list) else []


def save(name: str, items: list) -> None:
    """
    Save list data safely to JSON.
    """

    DATA_DIR.mkdir(exist_ok=True)

    path = _path(name)

    temp_path = path.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(items, file, indent=2, ensure_ascii=False)

    temp_path.replace(path)


# =========================
# ID GENERATION
# =========================


def next_id(name: str, key: str, prefix: str, width: int = 3) -> str:

    highest = 0

    for item in load(name):
        value = str(item.get(key, ""))

        if value.startswith(prefix) and value[len(prefix) :].isdigit():
            number = int(value[len(prefix) :])

            highest = max(highest, number)

    return f"{prefix}{highest + 1:0{width}d}"


# =========================
# DATE / TIME HELPERS
# =========================


def today_str() -> str:

    return date.today().strftime(DATE_FORMAT)


def parse_date(text):
    """
    Convert YYYY-MM-DD text to date.

    Returns None if invalid.
    """

    try:
        return datetime.strptime(text.strip(), DATE_FORMAT).date()

    except (ValueError, AttributeError, TypeError):
        return None


def parse_time(text):
    """
    Validate time and return HH:MM.
    """

    try:
        return datetime.strptime(text.strip(), "%H:%M").strftime("%H:%M")

    except (ValueError, AttributeError, TypeError):
        return None


def add_months(current_date: date, months: int) -> date:

    index = current_date.month - 1 + months

    year = current_date.year + index // 12

    month = index % 12 + 1

    day = min(current_date.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def money(amount) -> str:

    return f"€{float(amount):,.2f}"


# =========================
# MEMBER LOOKUPS
# =========================


def get_member(member_id: str):

    return next(
        (member for member in load("members") if (member["member_id"] == member_id)),
        None,
    )


def member_name(member_id: str) -> str:

    member = get_member(member_id)

    return member["name"] if member else member_id


# =========================
# TRAINER LOOKUPS
# =========================


def get_trainer(trainer_id: str):

    return next(
        (
            trainer
            for trainer in load("trainers")
            if (trainer["trainer_id"] == trainer_id)
        ),
        None,
    )


def trainer_name(trainer_id: str) -> str:

    trainer = get_trainer(trainer_id)

    return trainer["name"] if trainer else "Unassigned"


# =========================
# MEMBERSHIP LOOKUPS
# =========================


def get_membership(membership_id: str):

    return next(
        (
            membership
            for membership in load("memberships")
            if (membership["membership_id"] == membership_id)
        ),
        None,
    )


def member_memberships(member_id: str, memberships=None) -> list:

    if memberships is None:
        memberships = load("memberships")

    return [
        membership
        for membership in memberships
        if (membership["member_id"] == member_id)
    ]


def latest_membership(member_id: str, memberships=None):

    owned = member_memberships(member_id, memberships)

    if not owned:
        return None

    return max(owned, key=lambda membership: membership["end_date"])


# =========================
# MEMBERSHIP STATUS
# =========================


def membership_status(membership: dict) -> str:
    """
    Returns:
    - Upcoming
    - Active
    - Expired
    - Invalid
    """

    try:
        membership_object = Membership.from_dict(membership)

        return membership_object.status

    except (KeyError, ValueError):
        return "Invalid"


def member_status(member_id: str, memberships=None) -> str:
    """
    Returns the overall membership
    status of a member.
    """

    owned = member_memberships(member_id, memberships)

    if not owned:
        return "No Membership"

    statuses = [membership_status(membership) for membership in owned]

    if "Active" in statuses:
        return "Active"

    if "Upcoming" in statuses:
        return "Upcoming"

    return "Expired"


# =========================
# MEMBERSHIP RENEWAL
# =========================


def renewal_start(member_id: str) -> date:
    """
    If the latest membership is still
    active/upcoming, renewal starts the
    day after its end date.

    Otherwise renewal starts today.
    """

    latest = latest_membership(member_id)

    if latest:
        end_date = parse_date(latest["end_date"])

        if end_date and end_date >= date.today():
            return end_date + timedelta(days=1)

    return date.today()


# =========================
# MEMBERSHIP OVERLAP
# =========================


def has_membership_overlap(member_id: str, new_start: date, new_end: date) -> bool:
    """
    Prevent a member from having
    overlapping membership periods.
    """

    memberships = member_memberships(member_id)

    for membership in memberships:
        old_start = parse_date(membership["start_date"])

        old_end = parse_date(membership["end_date"])

        if old_start is None or old_end is None:
            continue

        overlap = new_start <= old_end and new_end >= old_start

        if overlap:
            return True

    return False


# =========================
# CREATE MEMBERSHIP
# =========================


def create_membership(member_id: str, plan: str, start: date, method: str, amount=None):
    """
    Create a membership and automatically
    create its payment.

    Used for both:
    - New membership
    - Renewal
    """

    # -------------------------
    # Validate Member
    # -------------------------

    if not get_member(member_id):
        raise ValueError("Member does not exist")

    # -------------------------
    # Validate Plan
    # -------------------------

    if plan not in PLANS:
        raise ValueError("Invalid membership plan")

    # -------------------------
    # Validate Start Date
    # -------------------------

    if not isinstance(start, date):
        raise ValueError("Invalid membership start date")

    # -------------------------
    # Validate Payment Method
    # -------------------------

    if method not in PAYMENT_METHODS:
        raise ValueError("Invalid payment method")

    # -------------------------
    # Calculate End Date
    # -------------------------

    months = PLANS[plan]["months"]

    end = add_months(start, months) - timedelta(days=1)

    # -------------------------
    # Prevent Overlap
    # -------------------------

    if has_membership_overlap(member_id, start, end):
        raise ValueError("Member already has a membership covering this period")

    # -------------------------
    # Determine Price
    # -------------------------

    if amount is None:
        amount = PLANS[plan]["price"]

    # -------------------------
    # Create Membership Object
    # -------------------------

    membership = Membership(
        membership_id=next_id("memberships", "membership_id", "MS"),
        member_id=member_id,
        plan=plan,
        start_date=start.strftime(DATE_FORMAT),
        end_date=end.strftime(DATE_FORMAT),
    )

    # -------------------------
    # Save Membership
    # -------------------------

    memberships = load("memberships")

    memberships.append(membership.to_dict())

    save("memberships", memberships)

    # -------------------------
    # Create Automatic Payment
    # -------------------------

    try:
        payment = add_payment(
            member_id=member_id,
            membership_id=(membership.membership_id),
            amount=amount,
            payment_date=start.strftime(DATE_FORMAT),
            method=method,
        )

    except Exception:
        # -------------------------
        # Rollback Membership
        # if payment fails
        # -------------------------

        memberships = [
            item
            for item in memberships
            if (item["membership_id"] != membership.membership_id)
        ]

        save("memberships", memberships)

        raise

    return (membership, payment)


# =========================
# PAYMENTS
# =========================


def add_payment(
    member_id: str,
    membership_id: str,
    amount: float,
    payment_date: str,
    method: str,
) -> Payment:

    # -------------------------
    # Validate Member
    # -------------------------

    if not get_member(member_id):
        raise ValueError("Member does not exist")

    # -------------------------
    # Validate Membership
    # -------------------------

    membership = get_membership(membership_id)

    if membership is None:
        raise ValueError("Membership does not exist")

    # -------------------------
    # Membership must belong
    # to this member
    # -------------------------

    if membership["member_id"] != member_id:
        raise ValueError("Membership does not belong to this member")

    # -------------------------
    # Create Payment Object
    # -------------------------

    payment = Payment(
        payment_id=next_id("payments", "payment_id", "P"),
        member_id=member_id,
        membership_id=membership_id,
        amount=amount,
        payment_date=payment_date,
        payment_method=method,
    )

    # -------------------------
    # Save Payment
    # -------------------------

    payments = load("payments")

    payments.append(payment.to_dict())

    save("payments", payments)

    return payment


# =========================
# ATTENDANCE
# =========================


def open_attendance(member_id: str):

    return next(
        (
            attendance
            for attendance in load("attendance")
            if (
                attendance["member_id"] == member_id and not attendance.get("check_out")
            )
        ),
        None,
    )


def add_attendance(member_id: str, day: str, check_in: str):

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


# =========================
# DASHBOARD
# =========================


def dashboard_stats() -> dict:

    members = load("members")
    trainers = load("trainers")
    memberships = load("memberships")
    payments = load("payments")
    attendance = load("attendance")

    # -------------------------
    # Member Status Counts
    # -------------------------

    active_members = 0
    upcoming_members = 0
    expired_members = 0
    no_membership = 0

    for member in members:
        status = member_status(member["member_id"], memberships)

        if status == "Active":
            active_members += 1

        elif status == "Upcoming":
            upcoming_members += 1

        elif status == "Expired":
            expired_members += 1

        elif status == "No Membership":
            no_membership += 1

    # -------------------------
    # Membership Status Counts
    # -------------------------

    active_memberships = 0
    upcoming_memberships = 0
    expired_memberships = 0

    for membership in memberships:
        status = membership_status(membership)

        if status == "Active":
            active_memberships += 1

        elif status == "Upcoming":
            upcoming_memberships += 1

        elif status == "Expired":
            expired_memberships += 1

    # -------------------------
    # Today's Attendance
    # -------------------------

    today = date.today()

    today_attendance = sum(
        1 for record in attendance if record.get("date") == today.strftime(DATE_FORMAT)
    )

    # -------------------------
    # Revenue This Month
    # -------------------------

    monthly_revenue = 0.0

    for payment in payments:
        payment_date = parse_date(payment.get("payment_date", ""))

        if (
            payment_date
            and payment_date.year == today.year
            and payment_date.month == today.month
        ):
            monthly_revenue += float(payment.get("amount", 0))

    return {
        "total_members": len(members),
        "total_trainers": len(trainers),
        "active_members": active_members,
        "upcoming_members": upcoming_members,
        "expired_members": expired_members,
        "no_membership": no_membership,
        "active_memberships": active_memberships,
        "upcoming_memberships": upcoming_memberships,
        "expired_memberships": expired_memberships,
        "today_attendance": today_attendance,
        "monthly_revenue": monthly_revenue,
    }


def recent_activity(limit: int = 10) -> list[str]:

    events = []

    today = date.today()

    # =========================
    # PAYMENTS
    # =========================

    for payment in load("payments"):
        payment_date = parse_date(payment.get("payment_date", ""))

        if payment_date is None:
            continue

        events.append(
            {
                "date": datetime.combine(payment_date, datetime.min.time()),
                "text": (
                    f"Payment {payment['payment_id']} - "
                    f"{member_name(payment['member_id'])} - "
                    f"{money(payment['amount'])} - "
                    f"{payment['payment_method']}"
                ),
            }
        )

    # =========================
    # ATTENDANCE
    # =========================

    for record in load("attendance"):
        attendance_date = parse_date(record.get("date", ""))

        check_in = parse_time(record.get("check_in", ""))

        if attendance_date is None:
            continue

        if check_in:
            event_time = datetime.strptime(check_in, "%H:%M").time()

        else:
            event_time = datetime.min.time()

        events.append(
            {
                "date": datetime.combine(attendance_date, event_time),
                "text": (
                    f"Attendance {record['attendance_id']} - "
                    f"{member_name(record['member_id'])} - "
                    f"Check in {record.get('check_in', '-')}"
                ),
            }
        )

    # =========================
    # MEMBERSHIP STARTS
    # =========================

    for membership in load("memberships"):
        start_date = parse_date(membership.get("start_date", ""))

        if start_date is None or start_date > today:
            continue

        events.append(
            {
                "date": datetime.combine(start_date, datetime.min.time()),
                "text": (
                    f"Membership {membership['membership_id']} - "
                    f"{member_name(membership['member_id'])} - "
                    f"{membership['plan']} - "
                    f"{membership_status(membership)}"
                ),
            }
        )

    # =========================
    # SORT
    # =========================

    events.sort(key=lambda event: event["date"], reverse=True)

    return [
        (f"{event['date'].strftime('%Y-%m-%d')} - {event['text']}")
        for event in events[:limit]
    ]

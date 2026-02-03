from flask import session, abort
from models import get_db


def get_user_role(username):
    """
    Fetch the user's role from the DB.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    db.close()
    return row[0] if row else None


def require_role(allowed_roles):
    """
    Enforce role-based access control.
    - Checks session login
    - Checks if user's role is in allowed list
    """
    username = session.get("username")
    if not username:
        abort(401)  # Not logged in

    user_role = get_user_role(username)
    if not user_role:
        abort(403)

    if user_role not in allowed_roles:
        abort(403)  # Forbidden

    return True


def valid_student(username):
    """
    Returns True only if the username exists in 'users' table AND is a student.
    Used in /add_record and /add_records validation.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT role FROM users WHERE username = %s", (username,))
    r = cur.fetchone()
    cur.close()
    db.close()

    return (r is not None) and (r[0] == "student")

import sqlite3
import unittest

from auth.service import AuthError, AuthService
from auth.throttle import LoginThrottle
from database.connection import init_database
from database.repository import UserRepository
from security.otp import OTPService
from utils.validation import ValidationError, validate_password_strength, validate_username

GOOD = "Str0ng!Pass"


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def make_service():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_database(conn)
    clock = Clock()
    svc = AuthService(
        repo=UserRepository(conn),
        throttle=LoginThrottle(max_failures=3, lock_seconds=60, clock=clock),
        otp=OTPService(max_attempts=3, ttl_seconds=120, clock=clock),
    )
    svc.register("alice", GOOD)
    return svc, clock


class ValidationTests(unittest.TestCase):
    def test_password_rules(self):
        validate_password_strength(GOOD)
        for bad in ("sh1!A", "alllowercase1!", "ALLUPPERCASE1!", "NoDigits!!", "NoSpecial123"):
            with self.assertRaises(ValidationError):
                validate_password_strength(bad)

    def test_password_over_72_bytes_is_rejected_not_crashed(self):
        with self.assertRaises(ValidationError):
            validate_password_strength("Aa1!" + "x" * 80)
        validate_password_strength("Aa1!" + "x" * 68)  # exactly 72 bytes

    def test_username_rules(self):
        validate_username("ok.name-1_")
        for bad in ("", "ab", "x" * 33, "has space", "semi;colon"):
            with self.assertRaises(ValidationError):
                validate_username(bad)

    def test_register_with_long_password_gives_a_clean_error(self):
        svc, _ = make_service()
        with self.assertRaises(AuthError):
            svc.register("bobby", "Aa1!" + "x" * 100)


class LoginTests(unittest.TestCase):
    def test_full_login(self):
        svc, _ = make_service()
        ch = svc.begin_login("alice", GOOD)
        self.assertEqual(svc.complete_login(ch.code).username, "alice")

    def test_wrong_password_same_message_for_unknown_user(self):
        svc, _ = make_service()
        with self.assertRaises(AuthError) as a:
            svc.begin_login("alice", "Wrong!Pass1")
        with self.assertRaises(AuthError) as b:
            svc.begin_login("nobody", "Wrong!Pass1")
        self.assertEqual(str(a.exception), str(b.exception))

    def test_lockout_after_repeated_failures_then_expires(self):
        svc, clock = make_service()
        for _ in range(3):
            with self.assertRaises(AuthError):
                svc.begin_login("alice", "Wrong!Pass1")
        with self.assertRaises(AuthError) as e:
            svc.begin_login("alice", GOOD)  # even the right password is refused
        self.assertIn("Try again in", str(e.exception))
        clock.now += 61
        self.assertTrue(svc.begin_login("alice", GOOD).code)

    def test_otp_dropped_after_three_wrong_codes(self):
        svc, _ = make_service()
        ch = svc.begin_login("alice", GOOD)
        wrong = "000000" if ch.code != "000000" else "111111"
        for _ in range(2):
            with self.assertRaises(AuthError) as e:
                svc.complete_login(wrong)
            self.assertIn("Incorrect code", str(e.exception))
        with self.assertRaises(AuthError):
            svc.complete_login(wrong)
        with self.assertRaises(AuthError):
            svc.complete_login(ch.code)  # the real code no longer works

    def test_otp_expires(self):
        svc, clock = make_service()
        ch = svc.begin_login("alice", GOOD)
        clock.now += 121
        with self.assertRaises(AuthError):
            svc.complete_login(ch.code)


if __name__ == "__main__":
    unittest.main()

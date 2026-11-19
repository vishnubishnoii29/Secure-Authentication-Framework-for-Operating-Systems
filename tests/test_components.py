import sqlite3
import unittest
from unittest import mock

from auth.service import AuthError
from auth.throttle import LoginThrottle
from database.connection import init_database
from database.repository import DuplicateUsernameError, UserRepository
from os_algorithms.cpu_scheduling import CPUScheduler, Process
from os_algorithms.deadlock_detection import DeadlockDetector, ResourceAllocationState
from security.hashing import hash_password, verify_password
from security.otp import OTPService
from tests.test_auth import GOOD, Clock, make_service


def make_repo():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_database(conn)
    return UserRepository(conn)


class RepositoryTests(unittest.TestCase):
    def test_create_and_find_ignores_case(self):
        repo = make_repo()
        repo.create_user("Alice", b"hash")
        rec = repo.get_by_username("alice")
        self.assertEqual((rec.username, rec.password_hash), ("Alice", b"hash"))

    def test_duplicate_username_is_rejected(self):
        repo = make_repo()
        repo.create_user("alice", b"h")
        with self.assertRaises(DuplicateUsernameError):
            repo.create_user("ALICE", b"h")

    def test_unknown_user_returns_none(self):
        self.assertIsNone(make_repo().get_by_username("nobody"))


class OTPTests(unittest.TestCase):
    def test_code_is_digits_of_right_length_and_single_use(self):
        otp = OTPService(length=6)
        ch = otp.issue("alice")
        self.assertRegex(ch.code, r"^\d{6}$")
        self.assertTrue(otp.verify("alice", ch.code))
        self.assertFalse(otp.verify("alice", ch.code))

    def test_wrong_user_and_expiry(self):
        clock = Clock()
        otp = OTPService(ttl_seconds=10, clock=clock)
        ch = otp.issue("alice")
        self.assertFalse(otp.verify("bob", ch.code))
        clock.now = 11
        self.assertFalse(otp.verify("alice", ch.code))
        self.assertFalse(otp.has_pending)


class ThrottleTests(unittest.TestCase):
    def test_lock_is_case_insensitive_and_success_resets(self):
        clock = Clock()
        t = LoginThrottle(max_failures=2, lock_seconds=30, clock=clock)
        t.record_failure("Alice")
        t.record_failure("alice")
        self.assertGreater(t.seconds_locked("ALICE"), 0)
        t.record_success("alice")
        self.assertEqual(t.seconds_locked("alice"), 0)


class HashingTests(unittest.TestCase):
    def test_round_trip_and_garbage_hash(self):
        h = hash_password(GOOD)
        self.assertTrue(verify_password(GOOD, h))
        self.assertFalse(verify_password("Other!Pass1", h))
        self.assertFalse(verify_password(GOOD, b"not-a-hash"))


class UnknownUserTimingTests(unittest.TestCase):
    def test_unknown_user_still_runs_a_bcrypt_check(self):
        svc, _ = make_service()
        with mock.patch("auth.service.verify_password", return_value=False) as check:
            with self.assertRaises(AuthError):
                svc.begin_login("nobody", GOOD)
        self.assertEqual(check.call_count, 1)


class MoreSchedulingTests(unittest.TestCase):
    def test_round_robin_gantt_and_idle_gap(self):
        r = CPUScheduler.round_robin([Process(0, 0, 3), Process(1, 10, 2)], 2)
        self.assertEqual(r.gantt_chart, [("P0", 0, 2), ("P0", 2, 3), ("P1", 10, 12)])
        self.assertEqual(r.waiting_times, {0: 0, 1: 0})

    def test_sjf_and_priority_reject_empty(self):
        for fn in (CPUScheduler.sjf, CPUScheduler.priority_scheduling):
            with self.assertRaises(ValueError):
                fn([])


class MoreDeadlockTests(unittest.TestCase):
    def test_need_matrix_and_safe_sequence_order(self):
        s = ResourceAllocationState(2, 1, [[1], [0]], [[2], [1]], [1])
        r = DeadlockDetector.detect_deadlock_bankers(s)
        self.assertEqual(r.need_matrix, [[1], [1]])
        self.assertEqual(r.safe_sequence, [0, 1])


if __name__ == "__main__":
    unittest.main()

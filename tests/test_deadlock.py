import unittest

from os_algorithms.deadlock_detection import DeadlockDetector as D
from os_algorithms.deadlock_detection import ResourceAllocationState as S


class DeadlockTests(unittest.TestCase):
    def test_bankers_textbook_is_safe(self):
        s = S(5, 3, [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
              [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]], [3, 3, 2])
        r = D.detect_deadlock_bankers(s)
        self.assertFalse(r.is_deadlock)
        self.assertEqual(sorted(r.safe_sequence), [0, 1, 2, 3, 4])

    def test_bankers_unsafe(self):
        r = D.detect_deadlock_bankers(S(2, 1, [[1], [1]], [[2], [2]], [0]))
        self.assertTrue(r.is_deadlock)
        self.assertEqual(r.deadlocked_processes, {0, 1})

    def test_wait_for_no_false_alarm_when_resources_free(self):
        r = D.detect_deadlock_wait_for_graph(S(2, 1, [[1], [1]], [[2], [2]], [5]))
        self.assertFalse(r.is_deadlock)

    def test_wait_for_cycle_lists_only_cycle_members(self):
        # P0 holds R0 wants R1, P1 holds R1 wants R0, P2 only waits on P0
        s = S(3, 2, [[1, 0], [0, 1], [0, 0]], [[1, 1], [1, 1], [1, 0]], [0, 0])
        r = D.detect_deadlock_wait_for_graph(s)
        self.assertTrue(r.is_deadlock)
        self.assertEqual(r.deadlocked_processes, {0, 1})

    def test_rejects_impossible_states(self):
        for bad in (
            S(1, 1, [[5]], [[2]], [0]),          # holds more than its maximum
            S(1, 1, [[0]], [[1]], [-1]),         # negative availability
            S(1, 2, [[0]], [[1, 1]], [0, 0]),    # short row
            S(0, 1, [], [], [0]),                # no processes
        ):
            with self.assertRaises(ValueError):
                D.detect_deadlock_bankers(bad)
            with self.assertRaises(ValueError):
                D.detect_deadlock_wait_for_graph(bad)


if __name__ == "__main__":
    unittest.main()

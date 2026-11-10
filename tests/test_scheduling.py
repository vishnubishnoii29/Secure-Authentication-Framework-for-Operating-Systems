import unittest

from os_algorithms.cpu_scheduling import CPUScheduler, Process

P = Process


class SchedulingTests(unittest.TestCase):
    def test_round_robin_textbook(self):
        r = CPUScheduler.round_robin([P(0, 0, 24), P(1, 0, 3), P(2, 0, 3)], 4)
        self.assertAlmostEqual(r.avg_waiting_time, 17 / 3)

    def test_fcfs_order_and_waits(self):
        r = CPUScheduler.fcfs([P(0, 0, 5), P(1, 1, 3), P(2, 2, 8), P(3, 3, 6)])
        self.assertEqual(r.waiting_times, {0: 0, 1: 4, 2: 6, 3: 13})

    def test_sjf_picks_shortest_available(self):
        r = CPUScheduler.sjf([P(0, 0, 5), P(1, 1, 3), P(2, 2, 8), P(3, 3, 6)])
        self.assertEqual([g[0] for g in r.gantt_chart], ["P0", "P1", "P3", "P2"])

    def test_priority_lower_number_first(self):
        r = CPUScheduler.priority_scheduling([P(0, 0, 4, 3), P(1, 0, 4, 1), P(2, 0, 4, 2)])
        self.assertEqual([g[0] for g in r.gantt_chart], ["P1", "P2", "P0"])

    def test_idle_gap_before_first_arrival(self):
        r = CPUScheduler.sjf([P(0, 5, 2)])
        self.assertEqual(r.gantt_chart, [("P0", 5, 7)])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            CPUScheduler.fcfs([])
        with self.assertRaises(ValueError):
            CPUScheduler.round_robin([P(0, 0, 1)], 0)


if __name__ == "__main__":
    unittest.main()

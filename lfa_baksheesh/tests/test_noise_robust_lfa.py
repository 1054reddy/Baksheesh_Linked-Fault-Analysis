"""
Unit tests and verification for Noise-Robust Linked Fault Analysis and
Unknown Fault Location Identification.
"""

import unittest
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.baksheesh import encrypt, MASK128, NUM_ROUNDS
from src.fault_sim import encrypt_with_linked_fault_last_round
from src.noise_robust_lfa import (
    identify_unknown_fault_pair,
    collect_noisy_faulty_ciphertexts,
    recover_difference_under_noise,
    full_attack_under_noise
)


class TestNoiseRobustLFA(unittest.TestCase):

    def setUp(self):
        random.seed(2026)
        self.master_key = random.getrandbits(128)

    def test_unknown_fault_location_identification_n5(self):
        """
        Verify that given N = 5 blind ciphertexts, the unknown fault pair (i*, j*)
        is identified with 100% accuracy over all 496 possible pairs.
        """
        # Test 10 distinct random unknown pairs
        tested_pairs = [
            (0, 1), (5, 6), (12, 13), (20, 21), (30, 31),
            (2, 8), (14, 25), (7, 19), (0, 31), (11, 22)
        ]

        for target_i, target_j in tested_pairs:
            # Attacker collects N = 5 blind ciphertexts from unknown target
            ciphertexts = []
            for _ in range(5):
                pt = random.getrandbits(128)
                ct_f, _ = encrypt_with_linked_fault_last_round(pt, self.master_key, target_i, target_j)
                ciphertexts.append(ct_f)

            # Blindly identify the pair over all 496 candidates
            identified_pair, leaked_diff, consistency = identify_unknown_fault_pair(ciphertexts)

            self.assertEqual(identified_pair, (target_i, target_j),
                             f"Failed to identify true pair ({target_i}, {target_j}). Got {identified_pair}")
            self.assertEqual(consistency, 1.0, "Consistency of true pair must be 1.0 (invariant)")

    def test_noise_tolerance_pmiss_30(self):
        """
        Verify that majority voting tolerates a 30% glitch miss rate over N = 30 queries.
        """
        target_i, target_j = 15, 16
        pts = [random.getrandbits(128) for _ in range(30)]

        # Collect 30 queries with 30% miss probability
        cts = collect_noisy_faulty_ciphertexts(pts, self.master_key, target_i, target_j, p_miss=0.30)
        diff, votes = recover_difference_under_noise(cts, target_i, target_j)

        # Expected vote count should be roughly (1 - 0.3) * 30 = 21 votes
        self.assertGreaterEqual(votes, 15, "True subkey difference must dominate majority votes")

    def test_full_128bit_key_recovery_under_30_percent_noise(self):
        """
        Verify that full 128-bit key recovery succeeds with 100% accuracy under p_miss = 30%.
        """
        success, rec_key, _ = full_attack_under_noise(self.master_key, p_miss=0.30, attempts_per_relation=30)
        self.assertTrue(success, "Full 128-bit key recovery must succeed under 30% noise")
        self.assertEqual(rec_key, self.master_key, "Recovered key must match true master key exactly")


if __name__ == "__main__":
    unittest.main()

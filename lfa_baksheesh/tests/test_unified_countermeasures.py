"""
Unit tests and empirical verification for Unified Countermeasures against
Linked Fault Analysis (LDFA and LIFA) on BAKSHEESH.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.baksheesh import encrypt, NUM_ROUNDS, MASK128
from src.constants import TEST_VECTORS
from src.countermeasure_unified import (
    ZeroRegisterBaksheeshDevice,
    ShuffledBaksheeshDevice,
    InfectiveBaksheeshDevice,
    UnifiedProtectedBaksheeshDevice
)


class TestUnifiedCountermeasures(unittest.TestCase):

    def setUp(self):
        self.master_key = int.from_bytes(os.urandom(16), "big") & MASK128
        self.plaintext = int.from_bytes(os.urandom(16), "big") & MASK128

    def test_compliance_with_standard(self):
        """Verify that all countermeasures produce bit-exact ciphertexts under normal operation."""
        unified_dev = UnifiedProtectedBaksheeshDevice(self.master_key)
        infective_dev = InfectiveBaksheeshDevice(self.master_key)

        expected_ct = encrypt(self.plaintext, self.master_key)
        self.assertEqual(unified_dev.encrypt_secure(self.plaintext), expected_ct)
        self.assertEqual(infective_dev.encrypt_infective(self.plaintext, 0, 1, fault_injected=False), expected_ct)

    def test_zero_register_defense(self):
        """
        Verify that Explicit Register Zeroing breaks the linked equality u' = v.
        When skipped, the target nibble becomes 0 instead of y[i].
        """
        dev = ZeroRegisterBaksheeshDevice(self.master_key)
        effective_count = 0
        ineffective_count = 0

        # Inject across 500 random plaintexts targeting pair (0, 1)
        for _ in range(500):
            pt = int.from_bytes(os.urandom(16), "big") & MASK128
            ct, is_ineff = dev.encrypt_with_fault(pt, 0, 1)
            if is_ineff:
                ineffective_count += 1
            else:
                effective_count += 1
                self.assertIsNone(ct)

        # Confirm that attacks are overwhelmingly detected/blocked
        self.assertGreater(effective_count, 0)
        self.assertEqual(dev.blocked_attacks, effective_count)

    def test_shuffled_sbox_defense(self):
        """
        Verify that S-box loop shuffling prevents deterministic adjacent-pair targeting.
        """
        dev = ShuffledBaksheeshDevice(self.master_key)
        observed_pairs = set()

        for step in range(50):
            pt = int.from_bytes(os.urandom(16), "big") & MASK128
            _, _, actual_pair = dev.encrypt_with_shuffled_fault(pt, target_step_k=5)
            observed_pairs.add(actual_pair)

        # Attacker targeted step 5 every time, but observed multiple distinct (i, j) pairs
        self.assertGreater(len(observed_pairs), 10, "Shuffling should distribute the fault across multiple pairs")

    def test_infective_defense(self):
        """
        Verify that infective computation corrupts the ciphertext and destroys algebraic leakage.
        """
        dev = InfectiveBaksheeshDevice(self.master_key)
        clean_ct = encrypt(self.plaintext, self.master_key)
        corrupted_ct = dev.encrypt_infective(self.plaintext, 0, 1, fault_injected=True)

        self.assertNotEqual(clean_ct, corrupted_ct, "Infective computation must corrupt the state")

    def test_unified_defense_complete_immunity(self):
        """
        Verify that the Unified Protected Device neutralizes the attack.
        """
        dev = UnifiedProtectedBaksheeshDevice(self.master_key)
        ct, action = dev.encrypt_under_attack(self.plaintext, target_pair=(0, 1))

        self.assertIn("DEFENSE_ACTIVE", action)
        self.assertEqual(dev.attack_failures, 1)


if __name__ == "__main__":
    unittest.main()

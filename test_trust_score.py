import unittest

from trust_score import (
    normalize_weights,
    calculate_weighted_score,
    determine_risk_level,
    generate_sha256,
    calculate_trust_score
)


class TestTrustScore(unittest.TestCase):

    def test_weight_normalization(self):

        weights = {
            "reliability": 2,
            "safety": 2,
            "fairness": 2,
            "privacy": 2,
            "transparency": 2,
            "robustness": 2
        }

        normalized = normalize_weights(weights)

        self.assertAlmostEqual(
            sum(normalized.values()),
            1.0
        )

    def test_weighted_score(self):

        scores = {
            "reliability": 100,
            "safety": 100,
            "fairness": 100,
            "privacy": 100,
            "transparency": 100,
            "robustness": 100
        }

        weights = {
            "reliability": 1/6,
            "safety": 1/6,
            "fairness": 1/6,
            "privacy": 1/6,
            "transparency": 1/6,
            "robustness": 1/6
        }

        score = calculate_weighted_score(
            scores,
            weights
        )

        self.assertEqual(
            score,
            100
        )

    def test_low_risk(self):

        self.assertEqual(
            determine_risk_level(95),
            "Low Risk"
        )

    def test_moderate_risk(self):

        self.assertEqual(
            determine_risk_level(80),
            "Moderate Risk"
        )

    def test_high_risk(self):

        self.assertEqual(
            determine_risk_level(60),
            "High Risk"
        )

    def test_sha256_generation(self):

        test_data = "trust-score"

        hash_value = generate_sha256(
            test_data
        )

        self.assertEqual(
            len(hash_value),
            64
        )

    def test_complete_calculation(self):

        scores = {
            "reliability": 90,
            "safety": 85,
            "fairness": 80,
            "privacy": 95,
            "transparency": 75,
            "robustness": 88
        }

        weights = {
            "reliability": 0.20,
            "safety": 0.20,
            "fairness": 0.15,
            "privacy": 0.15,
            "transparency": 0.15,
            "robustness": 0.15
        }

        result = calculate_trust_score(
            scores,
            weights
        )

        self.assertIn(
            "trust_score",
            result
        )

        self.assertIn(
            "risk_level",
            result
        )

        self.assertIn(
            "sha256",
            result
        )


if __name__ == "__main__":
    unittest.main()
import unittest
from server import evaluate_rules, RELEASE_MESSAGE


class RulesTests(unittest.TestCase):
    def test_version_message(self):
        self.assertEqual(RELEASE_MESSAGE, "rules v1")

    def test_ambient_conditions(self):
        self.assertEqual(evaluate_rules({"temperature": 22, "humidity": 45, "motion": False})["actions"], [])

    def test_hot_temperature(self):
        self.assertEqual(evaluate_rules({"temperature": 31})["actions"], ["enable_cooling"])

    def test_cold_temperature(self):
        self.assertEqual(evaluate_rules({"temperature": 15})["actions"], ["enable_heating"])

    def test_humidity_and_motion(self):
        self.assertEqual(evaluate_rules({"humidity": 76, "motion": True})["actions"],
                         ["enable_dehumidifier", "turn_on_light"])

    def test_invalid_json_shape(self):
        with self.assertRaises(ValueError):
            evaluate_rules([])

    def test_invalid_number_type(self):
        with self.assertRaises(ValueError):
            evaluate_rules({"temperature": "31"})


if __name__ == "__main__":
    unittest.main()

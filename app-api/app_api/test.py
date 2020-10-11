from django.test import TestCase


from app_api.cal import add, sub


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(3,8), 11)

    def test_subtract_numbers(self):
        """Values are subtracted and return"""
        self.assertEqual(sub(5, 11), 6)

    def test_cuper_long_fuckinton_that_should_be_flakeERROR(self):
        """Im so bored of this """
        self.assertAlmostEqual(sub(10,5),-4)
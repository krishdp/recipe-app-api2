from django.test import TestCase
from .calc import add, sub


class CalcTests(TestCase):
    def test_add(self):
        self.assertEqual(add(3, 8), 11)

    def test_sub(self):
        self.assertEqual(sub(5,2), 3)

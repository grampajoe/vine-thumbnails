import unittest

from app import get_vine_id


class TestVineID(unittest.TestCase):
    """Tests for Vine ID utils."""
    def test_get_vine_id(self):
        """Test getting a Vine ID"""
        # From a URL
        vine_id = get_vine_id('https://vine.co/v/hhmEEAIAzT2')
        self.assertEqual(vine_id, 'hhmEEAIAzT2')

        # From an ID
        vine_id = get_vine_id('hhmEEAIAzT2')
        self.assertEqual(vine_id, 'hhmEEAIAzT2')

        # From a bad string
        self.assertRaises(ValueError, get_vine_id, 'w?F@F#JFIJF')

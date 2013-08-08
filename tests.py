import unittest

from app import get_vine_id


class TestVineID(unittest.TestCase):
    """Tests for Vine ID utils."""
    def test_get_id_from_url(self):
        """Test getting a Vine ID from a URL"""
        url = 'https://vine.co/v/hhmEEAIAzT2'

        vine_id = get_vine_id(url)

        self.assertEqual(vine_id, 'hhmEEAIAzT2')

    def test_get_id_from_id(self):
        """Test getting an ID from an ID"""
        original_id = 'hhmEEAIAzT2'

        vine_id = get_vine_id(original_id)

        self.assertEqual(vine_id, original_id)

    def test_get_id_from_bad_string(self):
        """Test failing to get a Vine ID"""
        bad_string = 'w?F@F#JFIJF'

        self.assertRaises(ValueError, get_vine_id, bad_string)

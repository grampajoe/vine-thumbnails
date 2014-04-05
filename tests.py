import unittest
import mock

from app import get_vine_id, get_thumb_url


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


class TestVineThumb(unittest.TestCase):
    """Tests getting a vine thumb from a Vine page."""
    def test_get_thumb(self):
        """Should parse that thumb right out by golly."""
        vine = """
<html>
    <head>
        <title>This is totally real I promise</title>
    </head>
        <meta itemprop="thumbnailUrl" content="http://vine.co/thumb.jpg" />
    </body>
</html>
        """

        url = get_thumb_url(vine)

        self.assertEqual(url, 'http://vine.co/thumb.jpg')

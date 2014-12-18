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
    <body>
        <div itemprop="thumbnail" itemscope itemtype="http://schema.org/ImageObject">
            <meta itemprop="contentUrl" content="https://v.cdn.vine.co/r/videos/6D7618B85D1156201499773341696_3a4638806f4.1.3.15817004024158654826.mp4.jpg?versionId=DQtDP01Z6eY9FK.aahGNAlPPCEd85ZWM" />
        </div>
    </body>
</html>
        """

        url = get_thumb_url(vine)

        self.assertEqual(
            url,
            'https://v.cdn.vine.co/r/videos/6D7618B85D1156201499773341696_3a4638806f4.1.3.15817004024158654826.mp4.jpg?versionId=DQtDP01Z6eY9FK.aahGNAlPPCEd85ZWM'
        )

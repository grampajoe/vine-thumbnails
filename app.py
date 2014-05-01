from StringIO import StringIO
import re

from flask import (
    Flask, make_response, request, render_template, redirect, url_for)
import requests
from bs4 import BeautifulSoup
import newrelic.agent
from PIL import Image


app = Flask(__name__)


VINE_ID_PATTERN = re.compile(r'^\w+$')
VINE_URL_PATTERN = re.compile(r'vine.co/v/(\w+)')


def get_vine_id(string):
    """Get a Vine ID from a string.

    The string could either be a Vine ID already, or a Vine URL.
    """
    if VINE_ID_PATTERN.match(string):
        return string

    match = VINE_URL_PATTERN.search(string)
    if match:
        vine_id = match.group(1)
    else:
        raise ValueError('%s is not a valid Vine ID or URL.' % string)

    return vine_id


@app.route('/')
def index():
    """Renders a simple form for choosing a Vine and size."""
    vine_id_or_url = request.args.get('vine_id')
    size = request.args.get('s')

    if vine_id_or_url and size:
        try:
            vine_id = get_vine_id(vine_id_or_url)
        except ValueError:
            return '%s isn\'t a Vine ID or URL! Try again.' % vine_id_or_url

        return redirect(url_for('vine_thumb', vine_id=vine_id, s=size))

    return render_template('index.html')


def get_vine(vine_id):
    """Gets a vine!"""
    response = requests.get('http://vine.co/v/%s' % vine_id)

    if response.status_code != 200:
        abort(404)

    return response.content


def get_thumb_url(vine):
    """Parses a thumb URL right out of the vine!!!!"""
    parsed = BeautifulSoup(vine)
    return parsed.find('meta', itemprop='thumbnailUrl').attrs['content']


@app.route('/t/<vine_id>/')
def vine_thumb(vine_id):
    """Get a Vine video thumbnail.

    Add ?s=SIZE to the URL to specify the maximum width of the thumbnail.
    Vine "poster" images are 480x480.
    """
    vine = get_vine(vine_id)

    try:
        size = (int(request.args.get('s', 480)), 480)
    except ValueError:
        size = (480, 480)

    thumb_url = get_thumb_url(vine)

    thumb_response = requests.get(thumb_url)

    # Keep track of original file sizes on NewRelic for fun
    newrelic.agent.add_custom_parameter(
        'original_file_size',
        int(thumb_response.headers.get('content-length', 0)),
    )

    thumb_file = StringIO(thumb_response.content)
    thumb = Image.open(thumb_file)

    # Resize the poster and save it in a new StringIO
    thumb.thumbnail(size, Image.ANTIALIAS)
    saved_thumb = StringIO()
    thumb.save(saved_thumb, 'JPEG')

    response = make_response(saved_thumb.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'

    return response, 200


if __name__ == '__main__':
    app.run(debug=True)

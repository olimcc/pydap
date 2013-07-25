"""Test ASCII response."""

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from webtest import TestApp
from webob.headers import ResponseHeaders

from pydap.handlers.lib import BaseHandler
from pydap.tests.datasets import SimpleSequence, rain
from pydap.responses.ascii import ascii


class TestASCIIResponseSequence(unittest.TestCase):

    """Test ASCII response from a sequence."""

    def setUp(self):
        """Create a simple WSGI app for testing."""
        app = TestApp(BaseHandler(SimpleSequence))
        self.res = app.get('/.asc')

    def test_dispatcher(self):
        """Test the single dispatcher."""
        with self.assertRaises(StopIteration):
            ascii(None)

    def test_status(self):
        """Test the status code."""
        self.assertEqual(self.res.status, "200 OK")

    def test_content_type(self):
        """Test the content type."""
        self.assertEqual(self.res.content_type, "text/plain")

    def test_charset(self):
        """Test the charset."""
        self.assertEqual(self.res.charset, "utf-8")

    def test_headers(self):
        """Test headers from the response."""
        self.assertEqual(
            self.res.headers,
            ResponseHeaders([
                ('XDODS-Server', 'pydap/3.2'),
                ('Content-description', 'dods_ascii'),
                ('Content-type', 'text/plain; charset=utf-8'),
                ('Content-Length', '440')]))

    def test_body(self):
        """Test the generated ASCII response."""
        self.assertEqual(self.res.body, """Dataset {
    Sequence {
        String id;
        Int32 lon;
        Int32 lat;
        Int32 depth;
        Int32 time;
        Int32 temperature;
        Int32 salinity;
        Int32 pressure;
    } cast;
} SimpleSequence;
---------------------------------------------
cast.id, cast.lon, cast.lat, cast.depth, cast.time, cast.temperature, cast.salinity, cast.pressure
"1", 100, -10, 0, -1, 21, 35, 0
"2", 200, 10, 500, 1, 15, 35, 100

""")


class TestASCIIResponseGrid(unittest.TestCase):

    """Test ASCII response from a grid."""

    def test_body(self):
        """Test the generated ASCII response."""
        app = TestApp(BaseHandler(rain))
        res = app.get('/.asc')
        self.assertEqual(res.body, """Dataset {
    Grid {
        Array:
            Int32 rain[y = 2][x = 3];
        Maps:
            Int32 x[x = 3];
            Int32 y[y = 2];
    } rain;
} test;
---------------------------------------------
rain.rain
[0][0] 0
[0][1] 1
[0][2] 2
[1][0] 3
[1][1] 4
[1][2] 5

rain.x
[0] 0
[1] 1
[2] 2

rain.y
[0] 0
[1] 1


""")

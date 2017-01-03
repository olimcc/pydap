"""Test Pydap base exception."""

import sys
from pydap.exceptions import DapError
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestExceptions(unittest.TestCase):

    """Test Pydap base exception.

    Other exceptions behave exactly like the superclass, differing only by
    name, so no testing is required.

    """

    def test_dap_error(self):
        """Test the base exception."""
        exc = DapError("This is a test.")

        self.assertEqual(exc.value, "This is a test.")
        self.assertEqual(str(exc), repr("This is a test."))

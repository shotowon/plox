import sys

import pytest


def unit_tests():
    sys.exit(pytest.main(["tests"]))

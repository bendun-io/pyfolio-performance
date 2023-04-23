import unittest
from pyfolio_performance import Security


def test_mostrecentvalue():
    security = Security.getSecurityByIsin("DE0005190003")
    security.getMostRecentValue()
    assert True
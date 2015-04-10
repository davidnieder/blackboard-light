# -*- coding: utf-8 -*-

from unittest import TestSuite, TestLoader, TextTestRunner

from .view_tests_valid_requests import ViewTestsValid
from .view_tests_http_errors import ViewTestsHTTPErrors

view_tests = TestLoader().loadTestsFromTestCase(ViewTestsValid)
view_test_errors = TestLoader().loadTestsFromTestCase(ViewTestsHTTPErrors)

test_suite = TestSuite()
test_suite.addTests(view_tests)
test_suite.addTests(view_test_errors)

def run(verbosity=1):
    TextTestRunner(verbosity=verbosity).run(test_suite)


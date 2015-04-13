# -*- coding: utf-8 -*-

from unittest import TestSuite, TestLoader, TextTestRunner

from .view_tests_valid_requests import ViewTestsValid
from .view_tests_http_errors import ViewTestsHTTPErrors
from .api_tests import ApiTests

view_tests = TestLoader().loadTestsFromTestCase(ViewTestsValid)
view_test_errors = TestLoader().loadTestsFromTestCase(ViewTestsHTTPErrors)
api_tests = TestLoader().loadTestsFromTestCase(ApiTests)

test_suite = TestSuite()
test_suite.addTests(view_tests)
test_suite.addTests(view_test_errors)
test_suite.addTests(api_tests)

def run(verbosity=1):
    TextTestRunner(verbosity=verbosity).run(test_suite)


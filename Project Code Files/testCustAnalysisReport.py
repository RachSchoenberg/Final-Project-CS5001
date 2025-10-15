'''
Rachel Schoenberg
CS 5001
Fall 2024
Final Project
Testing CustomerAnalysisReport Class

Purpose:
- Test the integration of FrequencyRecency and MonetaryValue classes in the CustomerAnalysisReport.
- Validate data processing, monetary analysis, and visualization generation without using mock data.
'''

import unittest
from CustAnalysisReport import CustomerAnalysisReport

class TestCustomerAnalysisReport(unittest.TestCase):
    """
    Test cases for the CustomerAnalysisReport class.
    """

    def setUp(self):
        """
        Purpose: Initialize the CustomerAnalysisReport object with real Google Sheet credentials and setup data.
        """
        self.credentials_file = "/Users/raychellin/Desktop/Roux/5001/Final Project/Final Project Submission/Project Code Files/service_account.json"
        self.sheet_id = "15nOKtbo-01KZ_LY78MPvqUUka9ZeRNKJmyS_heujhsI"
        self.worksheet_names = ["Navis Cafe (May - October)", "Two Fat Cats Lancaster (May - October)"]
        self.current_month = 10

        self.report = CustomerAnalysisReport(
            credentials_file=self.credentials_file,
            sheet_id=self.sheet_id,
            worksheet_names=self.worksheet_names,
            current_month=self.current_month
        )

    def test_load_and_process_data(self):
        """
        Purpose: Test loading and processing of customer transaction data.
        """
        try:
            self.report.load_and_process_data()
            self.assertIsNotNone(self.report.all_data, "Data loading failed: all_data is None.")
            self.assertGreater(len(self.report.all_data), 0, "Data loading failed: all_data is empty.")
        except Exception as e:
            self.fail(f"load_and_process_data() raised an exception: {e}")

    def test_analyze_monetary_value(self):
        """
        Purpose: Test the monetary value analysis and action plan generation.
        """
        try:
            self.report.load_and_process_data()
            self.report.analyze_monetary_value()
            self.assertIsNotNone(self.report.monetary_value.monetary_data, "Monetary data is None.")
            self.assertIsNotNone(self.report.monetary_value.action_plan, "Action plan is None.")
            self.assertGreater(len(self.report.monetary_value.monetary_data), 0, "Monetary data is empty.")
        except Exception as e:
            self.fail(f"analyze_monetary_value() raised an exception: {e}")

    def test_generate_combined_visuals(self):
        """
        Purpose: Test the generation of combined visuals.
        """
        try:
            self.report.load_and_process_data()
            self.report.analyze_monetary_value()
            self.report.generate_combined_visuals()  # Should display visuals without errors.
        except Exception as e:
            self.fail(f"generate_combined_visuals() raised an exception: {e}")

    def test_generate_report(self):
        """
        Purpose: Test the generation of the full customer analysis report.
        """
        try:
            self.report.load_and_process_data()
            self.report.analyze_monetary_value()
            self.report.generate_report()  # Should generate a full report without errors.
        except Exception as e:
            self.fail(f"generate_report() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()

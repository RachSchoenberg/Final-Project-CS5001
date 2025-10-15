"""
Rachel Schoenberg
CS 5001
Fall 2024
Final Project
Testing FrequencyRecency Class

Must test:
* Input Validation:
- Ensure data argument is valid DataFrame with required columns (CustomerID, Paid Date, Amount).
- Handle missing or invalid data gracefully.

* Method Testing:
- create_customer_id:
~ Verify unique IDs are created for all transactions.
~ Ensure IDs are consistent for same card digits or transaction details.
- calculate_monthly_visits:
~ Validate correct calculation of visits per customer by month.
~ Handle different date formats and missing data.
- calculate_recency:
~ Confirm correct identification of most recent visits.
~ Test handling of missing or corrupted dates.
- categorize_customers:
~ Ensure customers are categorized correctly based on frequency and recency.
~ Validate categories are assigned accurately for all edge cases.

* Edge Cases:
- Empty DataFrame input.
- Single customer with multiple transactions.
- Missing columns in input data.
- Extremely large datasets for scalability.

* Performance Testing: Benchmark method performance on large datasets.
"""

import unittest
import pandas as pd
from FreRecAnalysis import FrequencyRecency


class TestFrequencyRecency(unittest.TestCase):
    """
    Test cases for the FrequencyRecency class.
    """

    def setUp(self):
        """
        Purpose: Initialize the test class and prepare sample data.

        New syntax:
            - pandas for creating and manipulating DataFrames.
            - FrequencyRecency class instantiation for testing.
        
        Summary:
            - Initializes the FrequencyRecency class with fake credentials and mock data to simulate workflow scenarios.
        """
        self.credentials_file = "fake_credentials.json"
        self.sheet_id = "fake_sheet_id"
        self.worksheet_names = ["Worksheet1", "Worksheet2"]
        self.current_month = 10
        self.frequency_recency = FrequencyRecency(
            credentials_file=self.credentials_file,
            sheet_id=self.sheet_id,
            worksheet_names=self.worksheet_names,
            current_month=self.current_month,
        )

        # Mock data for testing
        self.sample_data = pd.DataFrame({
            "Paid Date": ["2024-10-01 10:00:00", "2024-09-15 14:00:00", "2024-08-20 17:00:00"],
            "Last 4 Card Digits": ["1234", "5678", ""],
            "Amount": ["25.00", "50.00", "75.00"],
            "Type": ["Credit", "Credit", "Cash"],
        })

    def test_create_customer_id(self):
        """
        Purpose: Test creating unique customer IDs.

        New syntax:
            - pandas for copying and applying transformations on DataFrames.
            - lambda for generating customer IDs based on conditions.
        
        Summary:
            - Ensures that Customer IDs are created accurately by either using card digits or transaction details.
            - Validates consistency and uniqueness of the generated IDs.
        """
        result = self.frequency_recency.create_customer_id(self.sample_data)
        expected_ids = ["1234", "5678", "2024-08-20 17:00:00|75.00|Cash"]
        self.assertEqual(list(result["Customer ID"]), expected_ids)

    def test_calculate_monthly_visits(self):
        """
        Purpose: Test calculating monthly visit frequencies.

        New syntax:
            - pandas for datetime conversion, grouping, and aggregation.
        
        Summary:
            - Converts Paid Date to datetime and calculates the number of visits per month for each customer.
            - Validates the results for accuracy and ensures correct sorting by month.
        """
        self.sample_data["Paid Date"] = pd.to_datetime(self.sample_data["Paid Date"], errors="coerce")
        self.sample_data = self.frequency_recency.create_customer_id(self.sample_data)
        result = self.frequency_recency.calculate_monthly_visits(self.sample_data)

        # Sorting the results to ensure consistent order
        result_sorted = result.sort_values(by="Month").reset_index(drop=True)

        expected_months = sorted([10, 9, 8])  # Sort expected months for consistency
        self.assertEqual(result_sorted["Month"].tolist(), expected_months)
        self.assertEqual(result_sorted["Visits"].tolist(), [1, 1, 1])

    def test_calculate_recency(self):
        """
        Purpose: Test calculating the most recent visit date for each customer.

        New syntax:
            - pandas for datetime conversion, grouping, and finding maximum values.
        
        Summary:
            - Identifies the most recent transaction for each customer by grouping data.
            - Validates the functionality with a mock dataset to ensure accuracy.
        """
        self.sample_data["Paid Date"] = pd.to_datetime(self.sample_data["Paid Date"], format="%Y-%m-%d %H:%M:%S")
        self.sample_data = self.frequency_recency.create_customer_id(self.sample_data)
        result = self.frequency_recency.calculate_recency(self.sample_data)
        self.assertEqual(result["Recency"].max(), pd.Timestamp("2024-10-01 10:00:00"))

    def test_categorize_customers(self):
        """
        Purpose: Test categorizing customers into different categories.

        New syntax:
            - pandas for merging and aggregating DataFrames.
            - dictionary to store categorized customer counts.
        
        Summary:
            - Combines frequency and recency data to categorize customers into four groups:
                - Active Regular, Inactive Regular, Active Occasional, and Inactive Occasional.
            - Ensures accuracy of categorization logic with mock data.
        """
        self.sample_data["Paid Date"] = pd.to_datetime(self.sample_data["Paid Date"], format="%Y-%m-%d %H:%M:%S")
        self.sample_data = self.frequency_recency.create_customer_id(self.sample_data)

        monthly_visits = self.frequency_recency.calculate_monthly_visits(self.sample_data)
        recency_data = self.frequency_recency.calculate_recency(self.sample_data)
        categories = self.frequency_recency.categorize_customers(monthly_visits, recency_data)

        # Assert that all categories exist
        self.assertIn("Active Regular", categories)
        self.assertIn("Inactive Regular", categories)
        self.assertIn("Active Occasional", categories)
        self.assertIn("Inactive Occasional", categories)

    def test_main(self):
        """
        Purpose: Test the main method workflow.

        New syntax:
            - pandas for combining multiple DataFrames and applying custom methods.
        
        Summary:
            - Simulates the full workflow of the FrequencyRecency class, including data loading,
              processing, and categorization.
            - Validates integration between methods and consistency of the processed data.
        """
        # Use sample data to simulate main execution
        self.frequency_recency.all_data = self.sample_data
        self.frequency_recency.all_data = self.frequency_recency.create_customer_id(self.sample_data)

        # Execute workflow
        monthly_visits = self.frequency_recency.calculate_monthly_visits(self.frequency_recency.all_data)
        recency_data = self.frequency_recency.calculate_recency(self.frequency_recency.all_data)
        categories = self.frequency_recency.categorize_customers(monthly_visits, recency_data)

        # Check results
        self.assertTrue("Customer ID" in self.frequency_recency.all_data.columns)
        self.assertIsNotNone(categories)


if __name__ == "__main__":
    unittest.main()

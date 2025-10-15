'''
Rachel Schoenberg
CS 5001
Fall 2024
Final Project
Testing Monetary Class

Must test:
* Input Validation:
- Ensure data argument is valid DataFrame with required columns (CustomerID, TotalSpent)
- Handle missing or invalid data

* Method Testing:
- calculate_monetary_value:
~ Verify correct ranking 
~ Ensure returned DataFrame is sorted by TotalSpent in descending order
get_top_customers:
~ Validate correct number of top customers returned
~ Confirm output consistency for varying top_n values
- generate_action_plan:
~ Test if generates meaningful action plans based on customer data
~ Validates correct segmentation of customers into top_spenders, above_average_spenders, & low_spenders

* Edge Cases:
- Empty DataFrame input
- Single customer in the dataset
- Ties in monetary value for ranking
- Extremely large datasets to check performance

* Performance Testing: Benchmark method performance on large customer datasets

* Integration Testing: Ensures interaction with FrequencyRecency class when both are used
'''
import unittest
import pandas as pd
from MVAnalysis import MonetaryValue

class TestMonetaryValue(unittest.TestCase):
    def setUp(self):
        """
        Purpose: Set up test data for the MonetaryValue class.

        New syntax:
            - pandas to create a mock DataFrame for testing.
            - unittest for testing class setup.

        Summary:
            - Initializes the MonetaryValue class with mock customer data containing Customer IDs and spending amounts.
        """
        self.test_data = pd.DataFrame({
            "Customer ID": ["C1", "C2", "C3", "C4", "C5"],
            "Amount": [1500, 800, 300, 50, 1200]
        })
        self.monetary_value = MonetaryValue(self.test_data)

    def test_calculate_monetary_value(self):
        """
        Purpose: Test that total monetary values are calculated correctly.

        New syntax:
            - pandas for DataFrame grouping and aggregation.
            - unittest assertions to verify the calculation results.

        Summary:
            - Ensures the `calculate_monetary_value` method correctly computes the total monetary value for each customer.
            - Verifies the output DataFrame's size and specific values.
        """
        self.monetary_value.calculate_monetary_value()
        self.assertIsNotNone(self.monetary_value.monetary_data)
        self.assertEqual(len(self.monetary_value.monetary_data), 5)
        self.assertEqual(
            self.monetary_value.monetary_data.loc[
                self.monetary_value.monetary_data["Customer ID"] == "C1", "Total Monetary Value"
            ].values[0],
            1500
        )

    def test_identify_top_spending_customers(self):
        """
        Purpose: Test that top-spending customers are identified correctly.

        New syntax:
            - pandas for filtering the top spending customers.
            - unittest assertions for validating top customers' results.

        Summary:
            - Tests the `identify_top_spending_customers` method to ensure it selects the correct percentage of top spenders.
            - Validates the number and order of returned customers.
        """
        self.monetary_value.calculate_monetary_value()
        top_customers = self.monetary_value.identify_top_spending_customers(top_percent=40)
        self.assertEqual(len(top_customers), 2)  # 40% of 5 customers is 2
        self.assertEqual(top_customers.iloc[0]["Customer ID"], "C1")

    def test_generate_action_plan(self):
        """
        Purpose: Test that action plans are generated correctly based on monetary value.

        New syntax:
            - pandas for applying conditional logic to create action plans.
            - unittest assertions to validate the generated action plan DataFrame.

        Summary:
            - Tests the `generate_action_plan` method to ensure meaningful actions are assigned based on customer spending.
            - Verifies that the `Action` column exists and matches expected outputs for specific customers.
        """
        self.monetary_value.calculate_monetary_value()
        self.monetary_value.generate_action_plan()
        self.assertIsNotNone(self.monetary_value.action_plan)
        self.assertIn("Action", self.monetary_value.action_plan.columns)
        self.assertEqual(
            self.monetary_value.action_plan.loc[
                self.monetary_value.action_plan["Customer ID"] == "C1", "Action"
            ].values[0],
            "VIP Treatment: Personalized Offers"
        )

    def test_visualize_action_plans(self):
        """
        Purpose: Test that action plan visualization does not raise errors.

        New syntax:
            - matplotlib for generating bar charts for visualization.
            - unittest for exception handling during the visualization process.

        Summary:
            - Ensures that the `visualize_action_plans` method runs successfully without raising exceptions.
            - Validates the visualization functionality of the action plan distribution.
        """
        self.monetary_value.calculate_monetary_value()
        self.monetary_value.generate_action_plan()
        try:
            self.monetary_value.visualize_action_plans()
        except Exception as e:
            self.fail(f"visualize_action_plans() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()

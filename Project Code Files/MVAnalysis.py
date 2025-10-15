"""
Rachel Schoenberg
CS 5001
Fall 2024
Final Project
MonetaryValue Class

Goals:
- Calculate & rank customers based on monetary value
- Identify top-spending customers
- Provide actions to enhance customer retention & spending
- Generate action plan tailored to customer spending behavior

Arguments:
- all_data (pd.DataFrame): Combined data from all worksheets.
- spending_data (pd.DataFrame): Data containing spending details per customer.
- top_n (int, optional): Number of top customers to identify (default is 10).

Methods:
- calculate_total_spending: Computes total spending per customer.
- rank_top_customers: Ranks customers by total spending.
- generate_action_plan: Provides actionable insights for top customers.
- visualize_action_plans: Creates a visualization for top-spending customers.
"""

# Pandas library to utilize DataFrames
import pandas as pd
# Matplotlib library to create visualizations
import matplotlib.pyplot as plt
# FrequencyRecency Class
from FreRecAnalysis import FrequencyRecency


class MonetaryValue:
    """
    Purpose:
        Analyze and rank customers based on their monetary value, identify top spenders, 
        generate action plans for retention and spending enhancement, and visualize the data.
    """

    def __init__(self, all_data):
        """
        Purpose: Initialize the MonetaryValue class with the provided customer data.

        Params:
            - all_data (pd.DataFrame): Combined data with Customer IDs and transaction details.

        New syntax:
            - pandas to copy the DataFrame for processing.
        
        Summary:
            - Prepares the `all_data` DataFrame for monetary analysis and initializes placeholders
              for monetary and action plan data.
        """
        self.all_data = all_data.copy()
        self.monetary_data = None
        self.action_plan = None

    def calculate_monetary_value(self):
        """
        Purpose: Calculate the total monetary value for each customer.

        Params: None
        Returns: None (Updates self.monetary_data with total monetary value for each customer.)

        New syntax:
            - pandas for grouping data by Customer ID, summing, and sorting.

        Summary:
            - Groups transactions by Customer ID and computes their total spending.
            - Stores the resulting data in `self.monetary_data` and sorts by descending order.
        """
        self.all_data["Amount"] = pd.to_numeric(self.all_data["Amount"], errors="coerce")
        self.monetary_data = (
            self.all_data.groupby("Customer ID")["Amount"].sum().reset_index(name="Total Monetary Value")
        )
        self.monetary_data.sort_values(by="Total Monetary Value", ascending=False, inplace=True)

    def identify_top_spending_customers(self, top_percent=10):
        """
        Purpose: Identify the top-spending customers based on monetary value.

        Params:
            - top_percent (float): The percentage of top spenders to identify (default is 10%).

        Returns:
            - pd.DataFrame: DataFrame of top-spending customers.

        New syntax:
            - pandas to filter top rows from the DataFrame.

        Summary:
            - Calculates the number of customers to include based on the provided percentage.
            - Returns a subset of the `self.monetary_data` for the top-spending customers.
        """
        if self.monetary_data is None:
            raise ValueError("Monetary value data has not been calculated. Call calculate_monetary_value() first.")
        
        top_n = int(len(self.monetary_data) * (top_percent / 100))
        return self.monetary_data.head(top_n)

    def generate_action_plan(self):
        """
        Purpose: Generate tailored action plans for customers based on their spending behavior.

        Params: None
        Returns: None (Updates self.action_plan with recommended actions for each customer.)

        New syntax:
            - pandas for applying transformations to create a new column.

        Summary:
            - Uses the monetary value to categorize customers into specific action plans.
            - Stores the action plan data in `self.action_plan`.
        """
        if self.monetary_data is None:
            raise ValueError("Monetary value data has not been calculated. Call calculate_monetary_value() first.")
        
        self.action_plan = self.monetary_data.copy()
        self.action_plan["Action"] = self.action_plan["Total Monetary Value"].apply(self._assign_action)

    def _assign_action(self, value):
        """
        Purpose: Assign an action plan based on the customer's monetary value.

        Params:
            - value (float): Total monetary value of a customer.

        Returns:
            - str: Recommended action.

        New syntax:
            - conditional logic for value segmentation.

        Summary:
            - Categorizes customers into action plans based on spending thresholds:
                - VIP Treatment, Upselling, Retention, or Engagement.
        """
        if value > 1000:
            return "VIP Treatment: Personalized Offers"
        elif 500 <= value <= 1000:
            return "Upselling: Discounts on Larger Purchases"
        elif 100 <= value < 500:
            return "Retention: Loyalty Rewards"
        else:
            return "Engagement: Marketing Emails or Social Media"

    def visualize_action_plans(self):
        """
        Purpose: Visualize the distribution of customer action plans as a bar chart.

        Params: None
        Returns: None (Displays a bar chart with action plan distribution.)

        New syntax:
            - matplotlib for creating bar charts and adding annotations.

        Summary:
            - Generates a bar chart showing the distribution of customers across action plans.
            - Annotates the bars with the number of customers in each category.
        """
        if self.action_plan is None:
            raise ValueError("Action plan has not been generated. Call generate_action_plan() first.")
        
        action_counts = self.action_plan["Action"].value_counts()
        colors = ["gold", "lightblue", "lightgreen", "salmon"]
        action_labels = action_counts.index

        plt.figure(figsize=(10, 6))
        bars = plt.bar(action_labels, action_counts, color=colors, edgecolor="black")

        # Add the number of customers underneath each bar
        for bar, count in zip(bars, action_counts):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 2,
                str(count),
                ha="center",
                fontsize=10
            )

        # Chart aesthetics
        plt.title("Customer Action Plan Distribution", fontsize=14)
        plt.xlabel("Action Plan", fontsize=12)
        plt.ylabel("Number of Customers", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()
        plt.show()
        plt.savefig("action_plan_distribution.png")

def main():
    """
    Purpose: Integrate FrequencyRecency and MonetaryValue analysis to process data and provide insights.

    New syntax:
        - pandas for integrating data between classes.
        - matplotlib for visualizations.

    Summary:
        - Combines FrequencyRecency and MonetaryValue analyses to process customer data.
        - Visualizes the spending behavior and action plans for business decision-making.
    """
    # Initialize FrequencyRecency class and process data
    frequency_recency = FrequencyRecency(
        sheet_id="15nOKtbo-01KZ_LY78MPvqUUka9ZeRNKJmyS_heujhsI",
        worksheet_names=["Navis Cafe (May - October)", "Two Fat Cats Lancaster (May - October)"],
        credentials_file="/Users/raychellin/Desktop/Roux/5001/Final Project/Final Project Submission/Project Code Files/service_account.json",
        current_month=10
    )
    frequency_recency.main()

    # Pass combined data to MonetaryValue class
    monetary_value = MonetaryValue(frequency_recency.all_data)
    monetary_value.calculate_monetary_value()

    # Identify top-spending customers
    top_customers = monetary_value.identify_top_spending_customers(top_percent=10)
    print("Top-Spending Customers:")
    print(top_customers)

    # Generate action plans and visualize
    monetary_value.generate_action_plan()
    monetary_value.visualize_action_plans()


if __name__ == "__main__":
    main()

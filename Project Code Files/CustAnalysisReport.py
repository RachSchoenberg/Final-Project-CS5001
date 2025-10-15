'''
Rachel Schoenberg  
CS 5001  
Fall 2024  
Final Project  
CustomerAnalysisReport Class  

Goals:  
- Integrates FrequencyRecency and MonetaryValue classes to analyze customer behavior.  
- Combines frequency, recency, and monetary value analyses to generate a cohesive report.  
- Displays visual insights and textual summaries to assist business decision-making.  

Attributes:  
- credentials_file (str): Path to the Google API credentials file.  
- sheet_id (str): Google Sheet ID.  
- worksheet_names (list): List of worksheet/tab names in the Google Sheet.  
- current_month (int): The current month for analysis.  
- frequency_recency (FrequencyRecency): Instance of FrequencyRecency for processing frequency and recency data.  
- monetary_value (MonetaryValue): Instance of MonetaryValue for analyzing customer spending.  
- all_data (pd.DataFrame): Combined DataFrame containing all processed customer transaction data.  

Methods:  
- load_and_process_data(): Loads and processes customer transaction data using the FrequencyRecency class.  
- analyze_monetary_value(): Analyzes customer spending data and generates action plans using the MonetaryValue class.  
- generate_combined_visuals(): Creates a combined visual report with insights into visits, spending, and trends.  
- generate_report(): Produces a comprehensive customer analysis report with visuals and summaries.  
- main(): Orchestrates the entire workflow and generates the final report.  
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from FreRecAnalysis import FrequencyRecency
from MVAnalysis import MonetaryValue

class CustomerAnalysisReport:
    """
    Purpose:
        Combine analyses from FrequencyRecency and MonetaryValue classes into a cohesive summary report.
    Goals:
        - Generate visual insights to help business owners understand their customer data.
        - Provide actionable insights into customer categorization, monetary value, and spending behavior.
        - Save a report with visuals and key findings for business decision-making.
    """

    def __init__(self, credentials_file, sheet_id, worksheet_names, current_month):
        """
        Purpose: Initialize the CustomerAnalysisReport class with the required parameters.

        Params:
            - credentials_file (str): Path to the Google API credentials file.
            - sheet_id (str): Google Sheet ID.
            - worksheet_names (list of str): List of worksheet names to fetch data from.
            - current_month (int): The current month for analysis.

        New syntax:
            - Class attributes to store file paths, sheet details, and processed data.

        Summary:
            - Initializes the necessary attributes and dependencies for customer analysis.
        """
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id
        self.worksheet_names = worksheet_names
        self.current_month = current_month
        self.frequency_recency = None
        self.monetary_value = None
        self.all_data = None

    def load_and_process_data(self):
        """
        Purpose: Load and process data using FrequencyRecency class.

        Params: None

        Returns: None

        New syntax:
            - Instantiates the FrequencyRecency class for data processing.
            - Calls the `main()` method to aggregate and prepare data.

        Summary:
            - Loads transaction data from Google Sheets using the FrequencyRecency class.
            - Aggregates and processes data into a unified format for further analysis.
        """
        self.frequency_recency = FrequencyRecency(
            credentials_file=self.credentials_file,
            sheet_id=self.sheet_id,
            worksheet_names=self.worksheet_names,
            current_month=self.current_month
        )
        self.frequency_recency.main()
        self.all_data = self.frequency_recency.all_data

    def analyze_monetary_value(self):
        """
        Purpose: Analyze monetary value using MonetaryValue class.

        Params: None

        Returns: None

        New syntax:
            - Instantiates the MonetaryValue class for customer spending analysis.
            - Calls methods to calculate spending and generate action plans.

        Summary:
            - Analyzes customer spending data.
            - Generates actionable plans for customer retention and upselling strategies.
        """
        self.monetary_value = MonetaryValue(self.all_data)
        self.monetary_value.calculate_monetary_value()
        self.monetary_value.generate_action_plan()

    def generate_combined_visuals(self):
        """
        Purpose: Combine key visuals into a single page.

        Params: None

        Returns: None (Displays a single figure with visuals.)

        New syntax:
            - Matplotlib for bar charts and pie charts.
            - Seaborn for heatmap visualization.
            - Pandas for data preparation.

        Summary:
            - Creates a cohesive visual report.
            - Displays trends, spending behavior, and customer segmentation insights.
        """
        # Prepare data
        monthly_visits = self.frequency_recency.calculate_monthly_visits(self.all_data)
        recency_data = self.frequency_recency.calculate_recency(self.all_data)
        customer_categories = self.frequency_recency.categorize_customers(monthly_visits, recency_data)
        action_plan = self.monetary_value.action_plan

        # Time of Day by Time of Week heatmap data preparation
        self.all_data["Paid Date"] = pd.to_datetime(self.all_data["Paid Date"], errors="coerce")
        self.all_data["Hour"] = self.all_data["Paid Date"].dt.hour
        self.all_data["Weekday"] = self.all_data["Paid Date"].dt.day_name()

        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        trend_data = self.all_data.groupby(["Weekday", "Hour"]).size().reset_index(name="Orders")
        pivot_data = trend_data.pivot(index="Hour", columns="Weekday", values="Orders").fillna(0).reindex(columns=weekday_order)

        # Prepare figure with subplots
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle("Customer Analysis Report", fontsize=16)

        # Monthly Visits Bar Chart
        pivot_visits = monthly_visits.pivot(index="Customer ID", columns="Month", values="Visits").fillna(0)
        monthly_totals = pivot_visits.sum().reset_index()
        monthly_totals.columns = ["Month", "Total Visits"]
        
        axs[0, 0].bar(monthly_totals["Month"], monthly_totals["Total Visits"], color="lightblue", edgecolor="black")
        axs[0, 0].set_title("Monthly Visits by Customers (May - October)")
        axs[0, 0].set_xlabel("Month")
        axs[0, 0].set_ylabel("Total Visits")
        axs[0, 0].set_xticks(monthly_totals["Month"])
        axs[0, 0].set_xticklabels(["May", "June", "July", "August", "September", "October"])

        # Customer Categories Pie Chart
        categories = list(customer_categories.keys())
        values = list(customer_categories.values())
        axs[0, 1].pie(
            values, labels=categories, autopct="%1.1f%%", startangle=140, 
            colors=["gold", "lightcoral", "lightskyblue", "lightgreen"]
        )
        axs[0, 1].set_title("Customer Category Distribution")

        # Time of Day by Time of Week Heatmap
        sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="Blues", linewidths=0.5, ax=axs[1, 0])
        axs[1, 0].set_title("Order Trends by Time of Day and Week")
        axs[1, 0].set_xlabel("Day of the Week")
        axs[1, 0].set_ylabel("Hour of the Day")

        # Monetary Value Action Plan Bar Chart with Key
        action_counts = action_plan["Action"].value_counts()
        colors = ["gold", "lightblue", "lightgreen", "salmon"]
        reasons = [
            "VIP Treatment: Personalized Offers",
            "Upselling: Discounts on Larger Purchases",
            "Retention: Loyalty Rewards",
            "Engagement: Marketing Emails or Social Media"
        ]
        bars = axs[1, 1].bar(action_counts.index, action_counts, color=colors, edgecolor="black")
        axs[1, 1].set_title("Action Plan Distribution")
        axs[1, 1].set_xlabel("Action Plan")
        axs[1, 1].set_ylabel("Number of Customers")
        axs[1, 1].tick_params(axis="x", rotation=45)

        # Add number of customers on each bar
        for bar, count in zip(bars, action_counts):
            axs[1, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(count), ha="center", fontsize=10)

        # Add key for colors
        legend_patches = [plt.Line2D([0], [0], color=color, lw=10) for color in colors]
        axs[1, 1].legend(legend_patches, reasons, title="Action Plan", loc="upper right", fontsize=9)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

    def generate_report(self):
        """
        Purpose: Combine all analyses and visuals into a single report.

        Params: None

        Returns: None

        New syntax:
            - Combines visualizations with summary statistics.
            - Uses print statements for textual output.

        Summary:
            - Generates a report containing customer insights and visualizations.
        """
        self.generate_combined_visuals()

        # Summary report
        print("\n--- Summary Report ---")
        print("Customer Categories:", self.frequency_recency.categorize_customers(
            self.frequency_recency.calculate_monthly_visits(self.all_data),
            self.frequency_recency.calculate_recency(self.all_data)
        ))
        print("\nTop-Spending Customers:")
        print(self.monetary_value.identify_top_spending_customers(top_percent=10))
        print("\nAction Plans:")
        print(self.monetary_value.action_plan.head())


def main():
    """
    Purpose: Integrate all analyses and generate the customer analysis report.

    Params: None

    Returns: None

    New syntax:
        - Instantiates the CustomerAnalysisReport class.
        - Calls its methods to orchestrate the analysis workflow.

    Summary:
        - Acts as the main entry point for the application.
        - Executes all methods to produce a final report.
    """
    credentials_file = "/Users/raychellin/Desktop/Roux/5001/Final Project/Final Project Submission/Project Code Files/service_account.json"
    sheet_id = "15nOKtbo-01KZ_LY78MPvqUUka9ZeRNKJmyS_heujhsI"
    worksheet_names = ["Navis Cafe (May - October)", "Two Fat Cats Lancaster (May - October)"]
    current_month = 10

    report = CustomerAnalysisReport(credentials_file, sheet_id, worksheet_names, current_month)
    report.load_and_process_data()
    report.analyze_monetary_value()
    report.generate_report()


if __name__ == "__main__":
    main()

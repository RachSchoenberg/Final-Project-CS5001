'''
Rachel Schoenberg
CS 5001
Fall 2024
Final Project
FrequencyRecency Class

Goals:
- Loads customer data from a Google Sheet
- Stores data in Pandas DataFrame to analyze
- Find customers who pay in cash 
- Find customers who pay with a credit card
- Categorizes each customer as an active regular, active occasional, inactive regular, or inactive occasional
based on frequency of visits & recency of their last visit

Arguments:
- credentials_file (str): Path to the service account JSON credentials.
- sheet_id (str): The Google Sheet ID.
- worksheet_names (list): List of worksheet/tab names in the Google Sheet.
- current_month (int, optional): Current month for categorization (default is October).

Methods:
- get_data_from_google_sheet(sheet_id, worksheet_name, credentials_file): 
  Fetches data from a specific worksheet in a Google Sheet using gspread.
- create_customer_id(all_data): Creates a unique customer ID for each transaction based on card digits or transaction details.
- calculate_monthly_visits(all_data): Calculates the monthly visit frequencies for repeated customers.
- calculate_recency(all_data): Determines the most recent visit date for each customer.
- categorize_customers(frequency_data, recency_data): Categorizes customers as active/inactive regulars or occasionals based on frequency and recency.
- main(): Executes the entire data processing and customer categorization workflow.
'''

# Credentials class to authenticate access to Google Sheets (service account)
from google.oauth2.service_account import Credentials
# gspread library to interact with Google Sheets API
import gspread
# Pandas library to utilize DataFrames
import pandas as pd
# Datetime library to manipulate dates
import datetime
# Matplotlib library to create visualizations
import matplotlib.pyplot as plt

class FrequencyRecency:
    """
    Purpose:
        Analyze customer frequency and recency from transaction data, categorize customers, 
        and provide visualizations of the data.
    """
    def __init__(self, credentials_file, sheet_id, worksheet_names, current_month=10):
        """
        Purpose: Initialize the FrequencyRecency class with Google Sheet details and processing configurations.
        Params:
            - credentials_file (str): Path to the service account JSON credentials.
            - sheet_id (str): The Google Sheet ID.
            - worksheet_names (list): List of worksheet/tab names in the Google Sheet.
            - current_month (int): Current month for categorization (default is October).
        """
        self.credentials_file = credentials_file
        self.sheet_id = sheet_id
        self.worksheet_names = worksheet_names
        self.current_month = current_month
        self.all_data = None

    def get_data_from_google_sheet(self, sheet_id, worksheet_name, credentials_file):
        """
        Purpose: Fetch data from a specific worksheet in a Google Sheet using gspread.

        Params:
            - sheet_id (str): Google Sheet ID.
            - worksheet_name (str): Worksheet/tab name.
            - credentials_file (str): Path to the service account JSON credentials.

        Returns:
            - pd.DataFrame: DataFrame containing the worksheet data.

        New syntax:
            - gspread to connect to Google Sheets.
            - pandas to convert the worksheet data into a DataFrame.

        Summary:
            - This method uses the gspread library for authentication and fetches data from the specified Google Sheet worksheet. 
            - It converts the data into a Pandas DataFrame for further analysis.
        """

        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        rows = worksheet.get_all_records()
        return pd.DataFrame(rows)

    def create_customer_id(self, all_data):
        """
        Purpose: Create a unique customer ID for each transaction.

        Params:
            - all_data (pd.DataFrame): Combined data from all sheets.

        Returns:
            - pd.DataFrame: Data with Customer ID column added.

        New syntax:
            - pandas for data manipulation and column creation.
            - lambda function for conditional processing of data.

        Summary:
            - This method generates a `Customer ID` based on the last four digits of a card if available. 
            - For non-card payments, it creates an ID using the date, amount, and type of transaction.
        """

        all_data = all_data.copy()
        all_data["last_4_card_digits"] = all_data["Last 4 Card Digits"].fillna("").astype(str)
        all_data["Customer ID"] = all_data.apply(
            lambda x: x["last_4_card_digits"]
            if pd.notna(x["last_4_card_digits"]) and x["last_4_card_digits"].isdigit()
            else f"{x['Paid Date']}|{x['Amount']}|{x['Type']}",
            axis=1,
        )
        return all_data

    def calculate_monthly_visits(self, all_data):
        """
        Purpose: Calculate monthly visit frequencies for repeated customers.

        Params:
            - all_data (pd.DataFrame): Combined data with Customer IDs.

        Returns:
            - pd.DataFrame: Monthly visit frequencies for repeated customers.

        New syntax:
            - pandas to parse dates and group data by month and Customer ID.
            - groupby for aggregating monthly visits.

        Summary:
            - The method parses the transaction dates into datetime format and extracts the month.
            - It then groups data by `Customer ID` and `Month` to count the visits, returning the result as a DataFrame.
        """

        all_data["Paid Date"] = pd.to_datetime(all_data["Paid Date"], format="%m/%d/%y %I:%M %p", errors="coerce")
        all_data["Month"] = all_data["Paid Date"].dt.month
        monthly_visits = all_data.groupby(["Customer ID", "Month"]).size().reset_index(name="Visits")
        return monthly_visits

    def calculate_recency(self, all_data):
        """
        Purpose: Calculate the most recent visit date for each customer.

        Params:
            - all_data (pd.DataFrame): Combined data with Customer IDs.

        Returns:
            - pd.DataFrame: Recency data for all customers.

        New syntax:
            - pandas groupby to find the maximum date (most recent transaction) for each Customer ID.

        Summary:
            - This method calculates the most recent transaction date for each customer by grouping the data by `Customer ID`.
            - It provides a DataFrame with the latest visit date for every customer.
        """

        recency = all_data.groupby("Customer ID")["Paid Date"].max().reset_index(name="Recency")
        return recency

    def categorize_customers(self, frequency_data, recency_data):
        """
        Purpose: Categorize customers based on their frequency and recency.

        Params:
            - frequency_data (pd.DataFrame): Monthly visit frequencies for repeated customers.
            - recency_data (pd.DataFrame): Recency data for all customers.

        Returns:
            - dict: Categorized customer counts.

        New syntax:
            - pandas for data merging, grouping, and transformations.
            - dictionary to store customer categories.

        Summary:
            - Combines frequency and recency data to calculate total visits and categorize customers based on their behavior:
                - Active Regular, Inactive Regular, Active Occasional, and Inactive Occasional.
            - Customers are classified based on visit frequency and how recent their last transaction was.
        """

        customer_categories = {
            "Active Regular": 0,
            "Inactive Regular": 0,
            "Active Occasional": 0,
            "Inactive Occasional": 0,
        }

        data = pd.merge(frequency_data, recency_data, on="Customer ID", how="left")
        data["Total Visits"] = data.groupby("Customer ID")["Visits"].transform("sum")
        data["Recency Month"] = data["Recency"].dt.month

        for _, row in data.iterrows():
            if row["Total Visits"] > 6:
                if row["Recency Month"] == self.current_month:
                    customer_categories["Active Regular"] += 1
                else:
                    customer_categories["Inactive Regular"] += 1
            else:
                if row["Recency Month"] == self.current_month:
                    customer_categories["Active Occasional"] += 1
                else:
                    customer_categories["Inactive Occasional"] += 1

        return customer_categories

    def main(self):
        """
        Purpose: Execute the data processing and visualization workflow.

        Params:
            -  None

        Returns:
            - None

        New syntax:
            - pandas for data handling.
            - integration of helper methods to fetch, process, and categorize data.

        Summary:
            - Orchestrates the entire analysis pipeline:
                - Fetches data from Google Sheets.
                - Creates unique customer IDs.
                - Calculates visit frequencies and recency.
                - Categorizes customers into meaningful groups.
            - Prints the final customer categories for review.
        """

        try:
            # Fetch and combine data from Google Sheets
            data_frames = {}
            for worksheet_name in self.worksheet_names:
                data_frames[worksheet_name] = self.get_data_from_google_sheet(
                    self.sheet_id, worksheet_name, self.credentials_file
                )
            self.all_data = pd.concat(data_frames.values(), ignore_index=True)

            # Create Customer IDs
            self.all_data = self.create_customer_id(self.all_data)

            # Calculate monthly visits and recency
            monthly_visits = self.calculate_monthly_visits(self.all_data)
            recency_data = self.calculate_recency(self.all_data)

            # Categorize customers
            customer_categories = self.categorize_customers(monthly_visits, recency_data)
            print("Customer Categories:", customer_categories)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    frequency_recency = FrequencyRecency(
        credentials_file="/Users/raychellin/Desktop/Roux/5001/Final Project/Final Project Submission/Project Code Files/service_account.json",
        sheet_id="15nOKtbo-01KZ_LY78MPvqUUka9ZeRNKJmyS_heujhsI",
        worksheet_names=["Navis Cafe (May - October)", "Two Fat Cats Lancaster (May - October)"],
    )
    frequency_recency.main()

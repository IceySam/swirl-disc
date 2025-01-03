
import csv
import pandas as pd

import csv
import pandas as pd

class DataProcess:
    """
    A class to process various financial data metrics and append them to a DataFrame.

    Methods:
        - savings_consistency: Processes savings consistency metrics and appends them to the DataFrame.
        - repayment_behavior: Processes repayment behavior metrics and appends them to the DataFrame.
        - approval_rating: Processes approval rating metrics and appends them to the DataFrame.
        - loan_frequency: Processes loan frequency metrics and appends them to the DataFrame.
        - balance_change: Processes balance change metrics and appends them to the DataFrame.
    """

    def __init__(self):
        """
        Initializes the DataProcess class.
        """
        pass

    def savings_consistency(self, path, df):
        """
        Processes savings consistency metrics from a CSV file and appends them to the DataFrame.

        Args:
            path (str): The file path to the CSV containing savings consistency data.
            df (pd.DataFrame): The DataFrame to which the data will be appended.

        Returns:
            pd.DataFrame: The updated DataFrame with savings consistency data appended.
        """
        txn_ids, std_devs, consistency = [], [], []

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                txn_ids.append(row['txn_id'])
                std_devs.append(row['std_dev'])
                consistency.append(row['is_consistent'])

        df = df.assign(Txn_ids=txn_ids)
        df = df.assign(Std_devs=std_devs)
        df = df.assign(Consistency=consistency)

        return df

    def repayment_behavior(self, path, df):
        """
        Processes repayment behavior metrics from a CSV file and appends them to the DataFrame.

        Args:
            path (str): The file path to the CSV containing repayment behavior data.
            df (pd.DataFrame): The DataFrame to which the data will be appended.

        Returns:
            pd.DataFrame: The updated DataFrame with repayment behavior data appended.
        """
        txn_ids, proportions = [], []

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                txn_ids.append(row['txn_id'])
                proportions.append(row['proportion'])

        df = df.assign(Txn_ids=txn_ids)
        df = df.assign(Proportions=proportions)

        return df

    def approval_rating(self, path, df):
        """
        Processes approval rating metrics from a CSV file and appends them to the DataFrame.

        Args:
            path (str): The file path to the CSV containing approval rating data.
            df (pd.DataFrame): The DataFrame to which the data will be appended.

        Returns:
            pd.DataFrame: The updated DataFrame with approval rating data appended.
        """
        txn_ids, net_transaction_scores = [], []

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                txn_ids.append(row['txn_id'])
                net_transaction_scores.append(row['net_transaction_score'])

        df = df.assign(Txn_ids=txn_ids)
        df = df.assign(Net_transaction_scores=net_transaction_scores)

        return df

    def loan_frequency(self, path, df):
        """
        Processes loan frequency metrics from a CSV file and appends them to the DataFrame.

        Args:
            path (str): The file path to the CSV containing loan frequency data.
            df (pd.DataFrame): The DataFrame to which the data will be appended.

        Returns:
            pd.DataFrame: The updated DataFrame with loan frequency data appended.
        """
        txn_ids, avg_loan_times = [], []

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                txn_ids.append(row['txn_id'])
                avg_loan_times.append(row['avg_loan_time'])

        df = df.assign(Txn_ids=txn_ids)
        df = df.assign(Avg_loan_times=avg_loan_times)

        return df

    def balance_change(self, path, df):
        """
        Processes balance change metrics from a CSV file and appends them to the DataFrame.

        Args:
            path (str): The file path to the CSV containing balance change data.
            df (pd.DataFrame): The DataFrame to which the data will be appended.

        Returns:
            pd.DataFrame: The updated DataFrame with balance change data appended.
        """
        txn_ids, bal_changes = [], []

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                txn_ids.append(row['txn_id'])
                bal_changes.append(row['bal_change'])

        df = df.assign(Txn_ids=txn_ids)
        df = df.assign(Bal_changes=bal_changes)

        return df

    
        
# Example usage
# if __name__ == "__main__":
#     dp = DataProcess()
    
#     dataFrame = pd.DataFrame()
#     dataFrame = dp.savings_consistency(path="./data/savings_consistency.csv", df=dataFrame)
#     dataFrame = dp.repayment_behavior(path="./data/repay_behavior.csv", df=dataFrame)
#     dataFrame = dp.loan_frequency(path="./data/loan_frequency.csv", df=dataFrame)
#     dataFrame = dp.approval_rating(path="./data/approval_rating.csv", df=dataFrame)
#     dataFrame = dp.balance_change(path="./data/balance_change.csv", df=dataFrame)
    
#     print(dataFrame)
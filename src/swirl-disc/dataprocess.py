import csv
import pandas as pd

class DataProcess:
    """
    A class for processing data, specifically reading CSV files into Pandas DataFrames.

    Attributes:
        None

    Methods:
        csv_to_dataframe(path, headers): 
            Reads a CSV file and creates a Pandas DataFrame with specified headers.
    """

    def __init__(self):
        """
        Initializes an instance of the DataProcess class.
        """
        pass 

    def csv_to_dataframe(self, path, headers):
        """
        Reads a CSV file and creates a Pandas DataFrame with specified headers.

        Args:
            path: Path to the CSV file.
            headers: List of column names.

        Returns:
            Pandas DataFrame with the data from the CSV file.
        """

        data = [] 
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append([row[header] for header in headers]) 

        df = pd.DataFrame(data, columns=headers)
        return df
                

    
        
# Example usage
# if __name__ == "__main__":
#     dp = DataProcess()
    
#     sc_df = dp.csv_to_dataframe(path="./data/savings_consistency.csv", headers=['txn_id', 'std_dev', 'is_consistent', 'is_credit_worthy'])
#     rb_df = dp.csv_to_dataframe(path="./data/repay_behavior.csv", headers=['txn_id', 'proportion'])
#     ar_df = dp.csv_to_dataframe(path="./data/approval_rating.csv", headers=['txn_id', 'net_transaction_score'])
#     lf_df = dp.csv_to_dataframe(path="./data/loan_frequency.csv", headers=['txn_id', 'avg_loan_time'])
#     bc_df = dp.csv_to_dataframe(path="./data/balance_change.csv", headers=['txn_id', 'bal_change'])
    
#     print(sc_df)
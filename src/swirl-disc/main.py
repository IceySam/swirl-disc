from functools import reduce

import pandas as pd
import dataprocess
import modelling
import textprocess

def main():
    tp = textprocess.TextProcessor("./data/comments.csv", headers=['comment', 'polar', 'txn_id'], id_col='txn_id')
    dp = dataprocess.DataProcess()
    pl = modelling.Modelling()

    # load comment feature dataFrame
    df = tp.vector_features
    
    # append data dataFrame    
    sc_df = dp.csv_to_dataframe(path="./data/savings_consistency.csv", headers=['txn_id', 'std_dev', 'is_consistent', 'is_credit_worthy'])
    rb_df = dp.csv_to_dataframe(path="./data/repay_behavior.csv", headers=['txn_id', 'proportion'])
    ar_df = dp.csv_to_dataframe(path="./data/approval_rating.csv", headers=['txn_id', 'net_transaction_score'])
    lf_df = dp.csv_to_dataframe(path="./data/loan_frequency.csv", headers=['txn_id', 'avg_loan_time'])
    bc_df = dp.csv_to_dataframe(path="./data/balance_change.csv", headers=['txn_id', 'bal_change'])
    
    merged_df = reduce(lambda left, right: pd.merge(left, right, on='txn_id', how='outer'), [sc_df, rb_df, ar_df, lf_df, bc_df, df])
    
    # modeling
    cleaned_df = pl.clean(
        merged_df, 
        columns_to_drop=['txn_id'], 
        column_types= { 
            "std_dev": float,
            "is_consistent": int,
            "is_credit_worthy": int,
            "proportion": float,
            "avg_loan_time": float,
            "net_transaction_score": float,
        })

    pl.build_model(cleaned_df, target_col='is_credit_worthy')
    
if __name__ == "__main__":
    main()
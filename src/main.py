import dataprocess
import textprocess

def main():
    tp = textprocess.TextProcessor("./data/comments.csv")
    dp = dataprocess.DataProcess()

    # load comment feature dataFrame
    dataFrame = tp.vector_features
    
    # append data dataFrame
    dataFrame = dp.savings_consistency(path="./data/savings_consistency.csv", df=dataFrame)
    dataFrame = dp.repayment_behavior(path="./data/repay_behavior.csv", df=dataFrame)
    dataFrame = dp.loan_frequency(path="./data/loan_frequency.csv", df=dataFrame)
    dataFrame = dp.approval_rating(path="./data/approval_rating.csv", df=dataFrame)
    dataFrame = dp.balance_change(path="./data/balance_change.csv", df=dataFrame)
    
    print(dataFrame)

if __name__ == "__main__":
    main()
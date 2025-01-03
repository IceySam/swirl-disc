-- savings consistency
SELECT
	T.id 'txn_id',
    IFNULL(STDDEV(C.current_contribution), 0) AS std_dev,
    CASE
    	WHEN IFNULL(STDDEV(C.current_contribution), 0) <= IFNULL(AVG(C.current_contribution), 0) THEN TRUE
        ELSE FALSE
    END AS is_consistent
FROM
	transaction T LEFT JOIN 
    cooperator_account_logs C ON T.user_id=C.cooperatorId
WHERE
	(T.status='active' OR T.status='paid' OR T.status='declined') AND
    T.type='loan' AND
    T.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  -- Filter for the last year
GROUP BY
    T.id ORDER BY T.id ASC;

-- repayment behavior
SELECT
	T.id 'txn_id',
    R.repayment/T.amount AS proportion
FROM 
    transaction T
LEFT JOIN (
    SELECT 
        R.loan_id,
        COALESCE(SUM(K.amount), 0) AS repayment
    FROM 
        transaction K
    INNER JOIN 
        loan_repayment R 
        ON K.loanRepaymentId = R.id
    WHERE 
        K.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
        AND K.status = 'successful'
    GROUP BY 
        R.loan_id
) R 
ON R.loan_id = T.id
WHERE 
    (T.status='active' OR T.status='paid' OR T.status='declined') AND
    T.type='loan' AND
    T.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) ORDER BY T.id ASC;

-- net transaction score (approval rating)
SELECT
    T.id AS 'txn_id',
    (COUNT(CASE WHEN K.status IN ('active', 'paid') THEN 1 END) - 
     COUNT(CASE WHEN K.status = 'declined' THEN 1 END)) /
    COUNT(CASE WHEN K.status IN ('active', 'paid', 'declined') THEN 1 END) AS net_transaction_score
FROM
    transaction T
LEFT JOIN
    transaction K ON T.user_id = K.user_id AND K.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
WHERE
    T.status IN ('active', 'paid', 'declined') AND
    T.type = 'loan' AND
    T.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY
    T.id
ORDER BY
    T.id ASC;

-- loan application frequency
WITH
    AddContext AS (
        SELECT
            id AS txn_id,
            user_id,
            date_applied,
            date_disbursed,
            LAG(date_disbursed) OVER (PARTITION BY user_id ORDER BY date_disbursed) AS previous_date_disbursed
        FROM
            transaction
        WHERE
            status IN ('active', 'paid', 'declined')
            AND type = 'loan'
            AND created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    ),
    FilteredContext AS (
        SELECT
            txn_id,
            DATEDIFF(date_disbursed, previous_date_disbursed) AS time_diff
        FROM
            AddContext
    )
SELECT
    txn_id,
    AVG(time_diff) AS avg_loan_time
FROM
    FilteredContext
GROUP BY
    txn_id
ORDER BY
    txn_id ASC;

-- balance change
WITH
    SubContext AS (
        SELECT
            T.id AS txn_id,
        	B.balance_after - LAG(B.balance_after) OVER (PARTITION BY B.cooperatorAccountId ORDER BY B.balance_after) AS balance
        FROM
            transaction T
        LEFT JOIN 
        	balance_history B ON T.cooperator_account_id=B.cooperatorAccountId
        WHERE
            T.status IN ('active', 'paid', 'declined')
            AND T.type = 'loan'
            AND T.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    )
SELECT
    txn_id,
    SUM(balance) AS bal_change
FROM
    SubContext
GROUP BY
    txn_id
ORDER BY
    txn_id ASC;

-- comments
SELECT
  T.id AS txn_id,
  C.comment,
  CASE WHEN T.status IN ('active', 'paid') THEN TRUE ELSE FALSE END AS polar
FROM
  transaction T
LEFT JOIN (
    SELECT transactionId, comment, ROW_NUMBER() OVER (PARTITION BY transactionId ORDER BY id DESC) AS row_num
    FROM comments
  ) C ON T.id = C.transactionId AND C.row_num = 1
WHERE
  T.status IN ('active', 'paid', 'declined')
  AND T.type = 'loan'
  AND T.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
ORDER BY
  T.id ASC;
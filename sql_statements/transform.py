
ft_customer_transactions = '''
    INSERT INTO staging.ft_customer_transactions (
        transaction_id
        , date
        , customer_id
        , bank_id
        , recipient_id 
        , destination_account_number
        , description
        , amount_transferred
        , transaction_status
    )
    SELECT t.id, t.date, w.owner_id, c.issuer, t.recipient_id, t.destination_account_number, t.description, t.amount, ts.name
    FROM raw_data.transactions t
    LEFT JOIN raw_data.wallets w
        ON t.wallet_id = w.id
    LEFT JOIN raw_data.cards c
        ON w.associated_card = c.id
    LEFT JOIN raw_data.transaction_status ts
        ON t.transaction_status = ts.id;
'''

dim_wallets = '''
    INSERT INTO staging.dim_wallets (
        wallet_id
        , owner_id
        , wallet_number
        , current_balance
        , associated_card_id
        , created_at 
        , owner_name 
        , owner_status
        , associated_card_name
        , associated_card_number
        , expiry_date
        , associated_card_issuer
        , associated_card_date_added 
        , is_card_expired
    )
    SELECT w.id, w.owner_id, w.wallet_number, w.current_balance, w.associated_card, w.created_at, u.name, u.status, c.name_on_card, c.card_number, c.expiry_date, b.name, c.date_added, FALSE
    FROM raw_data.wallets w
    LEFT JOIN raw_data.users u
        ON w.owner_id = u.id
    LEFT JOIN raw_data.cards c
        ON w.associated_card = c.id
    LEFT JOIN raw_data.banks b
        ON b.id = c.issuer;

'''

dim_dates = '''
    INSERT INTO staging.dim_dates (
        date
        , year
        , month
        , day
        , quarter
        , is_weekend
    )
    SELECT t.date, EXTRACT(YEAR FROM t.date), EXTRACT(MONTH FROM t.date), EXTRACT(DAY FROM t.date), EXTRACT(QUARTER FROM t.date), CASE WHEN EXTRACT(WEEKDAY FROM t.date) IN (6,0) THEN true ELSE false END AS is_weekend
    FROM raw_data.transactions t;
'''

dim_customer = '''
    INSERT INTO staging.dim_customers (
    customer_id
    , name
    , email
    , bvn
    , bvn_verified
    , phone
    , phone_verified
    , address
    , address_verified      
    , username
    , registration_date
    , status
    , city
    , state
    , country
    )
    SELECT u.id
    , u.name
    , u.email
    , u.bvn
    , CASE WHEN (cvs.bvn_verified = 'true') THEN true ELSE false END AS bvn_verified
    , u.phone
    , CASE WHEN (cvs.phone_verified = 'true') THEN true ELSE false END AS phone_verified
    , u.address
    , CASE WHEN (cvs.address_verified = 'true') THEN true ELSE false END AS address_verified
    , u.username, u.registration_date, u.status, NULL, NULL, NULL
    FROM raw_data.users u
    LEFT JOIN raw_data.cust_verification_status cvs
        ON u.id = cvs.user_id;
'''

dim_banks = '''
INSERT INTO staging.dim_banks (
    bank_id
    , name
    , address
    , contact 
    , street
    , city
    , state
    , country
)
    SELECT b.id, b.name, b.address, b.contact, NULL, NULL, NULL, NULL
    FROM raw_data.banks b;
'''

transformation_queries = [ft_customer_transactions, dim_wallets, dim_dates, dim_customer, dim_banks]

# =============================================== FOR DEV SCHEMA
banks = '''CREATE TABLE IF NOT EXISTS raw_data.banks
(
    id integer PRIMARY KEY NOT NULL ,
    name character varying(25),
    address character varying(50),
    contact text
);'''

cards = '''CREATE TABLE IF NOT EXISTS raw_data.cards
(
    id integer PRIMARY KEY NOT NULL,
    owner_id integer,
    name_on_card VARCHAR(255),
    card_number VARCHAR(50),
    issuer integer,
    expiry_date VARCHAR,
    date_added date
);'''

cust_verification_status = '''
CREATE TABLE IF NOT EXISTS raw_data.cust_verification_status
(
    id integer PRIMARY KEY NOT NULL,
    user_id integer,
    bvn_verified VARCHAR(4),
    phone_verified VARCHAR(50),
    address_verified VARCHAR(50)
);
'''

transaction_status = '''
CREATE TABLE IF NOT EXISTS raw_data.transaction_status
(
    id integer PRIMARY KEY NOT NULL,
    name VARCHAR(10)
);
'''

transactions = '''
CREATE TABLE IF NOT EXISTS raw_data.transactions
(
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    wallet_id integer,
    amount numeric(8,2),
    description VARCHAR(37),
    date date,
    recipient_id VARCHAR DEFAULT NULL,
    destination_account_number bigint,
    destination_bank VARCHAR(23),
    transaction_status VARCHAR(1)
);
'''

users = '''
CREATE TABLE IF NOT EXISTS raw_data.users
(
    id integer PRIMARY KEY NOT NULL,
    name VARCHAR(18),
    email VARCHAR(50),
    phone VARCHAR(11),
    bvn bigint,
    address VARCHAR(39),
    username VARCHAR(50),
    registration_date date,
    status VARCHAR(8)
);
'''

wallets = '''
CREATE TABLE IF NOT EXISTS raw_data.wallets
(
    id integer PRIMARY KEY NOT NULL,
    owner_id integer,
    wallet_number bigint,
    current_balance numeric(8,2),
    associated_card integer,
    created_at date
);
'''


# =============================================== FOR STAR SCHEMA
ft_customer_transactions = '''
CREATE TABLE IF NOT EXISTS staging.ft_customer_transactions(
    id BIGINT IDENTITY(1, 1)
    , transaction_id VARCHAR NOT NULL
    , date DATE
    , customer_id VARCHAR
    , bank_id INT
    , recipient_id VARCHAR DEFAULT NULL
    , destination_account_number BIGINT
    , description TEXT
    , amount_transferred NUMERIC(8, 2)
    , transaction_status VARCHAR(30)
);
'''

dim_wallets = '''
    CREATE TABLE IF NOT EXISTS staging.dim_wallets (
        id BIGINT IDENTITY(1, 1)
        , wallet_id integer NOT NULL
        , owner_id integer
        , wallet_number bigint
        , current_balance numeric(8,2)
        , associated_card_id integer
        , created_at date
        , owner_name VARCHAR
        , owner_status VARCHAR
        , associated_card_name VARCHAR
        , associated_card_number VARCHAR
        , expiry_date VARCHAR
        , associated_card_issuer VARCHAR
        , associated_card_date_added DATE
        , is_card_expired BOOLEAN DEFAULT FALSE
    );
'''

dim_dates = '''
    CREATE TABLE IF NOT EXISTS staging.dim_dates (
        id BIGINT IDENTITY(1, 1)
        , date DATE
        , year INT
        , month INT
        , day INT
        , quarter VARCHAR
        , is_weekend BOOLEAN
    );
'''

dim_customer = '''
CREATE TABLE IF NOT EXISTS staging.dim_customers (
    id BIGINT IDENTITY(1, 1)
    , customer_id INT NOT NULL
    , name VARCHAR(18)
    , email VARCHAR(50)
    , bvn bigint
    , bvn_verified BOOLEAN
    , phone VARCHAR(11)
    , phone_verified BOOLEAN
    , address VARCHAR(39)
    , address_verified BOOLEAN
      
    , username VARCHAR(50)
    , registration_date DATE
    , status VARCHAR(8)
    , city VARCHAR
    , state VARCHAR
    , country VARCHAR
);
'''

dim_banks = '''
CREATE TABLE IF NOT EXISTS staging.dim_banks
(
    id BIGINT IDENTITY(1, 1)
    , bank_id integer NOT NULL
    , name VARCHAR(25)
    , address VARCHAR(50)
    , contact text
    , street VARCHAR
    , city VARCHAR
    , state VARCHAR
    , country VARCHAR
);
'''



raw_data_tables = [banks, cards, cust_verification_status, transaction_status, transactions, users, wallets]
transformed_tables = [ft_customer_transactions, dim_wallets, dim_dates, dim_customer, dim_banks]
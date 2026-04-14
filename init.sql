-- Criar sequência para tabela transactions
CREATE SEQUENCE transactions_id_seq;

-- Criar tabela transactions
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY DEFAULT nextval('transactions_id_seq'),
    type SMALLINT NOT NULL,
    date DATE NOT NULL,
    card_number VARCHAR(255) NOT NULL,
    national_id VARCHAR(255) NOT NULL,
    hour TIME NOT NULL,
    store_name VARCHAR(255) NOT NULL,
    store_owner VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

-- ============================================================
-- Debezium CDC User Setup
-- ============================================================

-- 1. Create CDC user
CREATE USER debezium
WITH PASSWORD 'debezium_pass';


-- 2. Allow the user to connect to the database
GRANT CONNECT ON DATABASE fraud_detection TO debezium;


-- 3. Allow logical replication
ALTER ROLE debezium WITH REPLICATION;


-- 4. Allow navigation/access to the public schema
GRANT USAGE ON SCHEMA public TO debezium;


-- 5. Allow Debezium to read the table during snapshot
GRANT SELECT ON TABLE public.transaction TO debezium;


-- 6. Create publication for Debezium
CREATE PUBLICATION dbz_publication
FOR TABLE public.transaction;
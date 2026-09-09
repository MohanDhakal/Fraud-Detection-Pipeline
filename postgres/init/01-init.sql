--
-- PostgreSQL database dump
--

\restrict hTC6VtNws9OJFrx1AMac3hNiHFYO6rFKX3ZaRjoi9uiggJZ4JS8U87spUatWMid

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction (
    id character varying(100) NOT NULL,
    customer_id character varying(100),
    amount numeric(19,0),
    "timestamp" timestamp without time zone,
    location_name character varying(50),
    ip_address character varying(24),
    currency character varying(5),
    device_id character varying,
    is_fraud boolean,
    fraud_type character varying(24),
    service_name character varying(24)
);


ALTER TABLE public.transaction OWNER TO postgres;

--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transaction (id, customer_id, amount, "timestamp", location_name, ip_address, currency, device_id, is_fraud, fraud_type, service_name) FROM stdin;
\.


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict hTC6VtNws9OJFrx1AMac3hNiHFYO6rFKX3ZaRjoi9uiggJZ4JS8U87spUatWMid


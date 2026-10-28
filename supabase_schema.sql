-- Supabase/PostgreSQL schema for the workflow automation backend.
-- Run this script in the Supabase SQL Editor.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SEQUENCE IF NOT EXISTS public.seq_cl_client_results
    AS bigint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE IF NOT EXISTS public.seq_cl_outreach_requests
    AS bigint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.cl_client_results (
    seq_id bigint NOT NULL
        DEFAULT nextval('public.seq_cl_client_results'::regclass),
    id uuid NOT NULL
        DEFAULT gen_random_uuid(),
    name varchar(255) NOT NULL,
    category varchar(100),
    address text,
    phone varchar(20),
    rating numeric(2, 1),
    google_map_url text,
    cold_message text,
    created_date timestamp with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    is_active boolean NOT NULL
        DEFAULT TRUE,
    CONSTRAINT cl_client_results_pkey PRIMARY KEY (seq_id)
);

CREATE TABLE IF NOT EXISTS public.cl_outreach_requests (
    seq_id bigint NOT NULL
        DEFAULT nextval('public.seq_cl_outreach_requests'::regclass),
    id uuid NOT NULL
        DEFAULT gen_random_uuid(),
    business1 varchar(255),
    business2 varchar(255),
    business3 varchar(255),
    location text,
    pitch text,
    search_place_count bigint NOT NULL
        DEFAULT 3,
    created_date timestamp with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    request_status varchar(50) NOT NULL
        DEFAULT 'pending',
    message text,
    CONSTRAINT cl_outreach_requests_pkey PRIMARY KEY (id),
    CONSTRAINT cl_outreach_requests_seq_id_key UNIQUE (seq_id),
    CONSTRAINT chk_search_place_count CHECK (search_place_count >= 0)
);

ALTER SEQUENCE public.seq_cl_client_results
    OWNED BY public.cl_client_results.seq_id;

ALTER SEQUENCE public.seq_cl_outreach_requests
    OWNED BY public.cl_outreach_requests.seq_id;

COMMENT ON TABLE public.cl_client_results IS
    'Stores scraped business details and generated outreach messages';

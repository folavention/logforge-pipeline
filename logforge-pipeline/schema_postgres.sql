-- schema_postgres.sql
-- PostgreSQL schema for LogForge-Observe migration

-- Drop existing tables if you are re-running the schema
DROP TABLE IF EXISTS logs_success;
DROP TABLE IF EXISTS logs_error;

-- Table for successful log entries (2xx–3xx status codes)
CREATE TABLE logs_success (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,  -- IPv4/IPv6
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_url TEXT NOT NULL,
    status_code INTEGER NOT NULL CHECK (status_code BETWEEN 200 AND 399),
    response_size BIGINT NOT NULL,
    referer TEXT,
    user_agent TEXT,
    hash TEXT UNIQUE NOT NULL, -- deduplication hash
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for error log entries (4xx–5xx status codes)
CREATE TABLE logs_error (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_url TEXT NOT NULL,
    status_code INTEGER NOT NULL CHECK (status_code BETWEEN 400 AND 599),
    response_size BIGINT NOT NULL,
    referer TEXT,
    user_agent TEXT,
    hash TEXT UNIQUE NOT NULL,
    inserted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes to improve query performance
CREATE INDEX idx_logs_success_timestamp ON logs_success (timestamp);
CREATE INDEX idx_logs_error_timestamp ON logs_error (timestamp);

CREATE INDEX idx_logs_success_status_code ON logs_success (status_code);
CREATE INDEX idx_logs_error_status_code ON logs_error (status_code);

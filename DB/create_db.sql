--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

--
-- Name: forecast_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE DATABASE  weather_db;

CREATE TABLE   forecast_user (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    password character varying(15) NOT NULL,
    last_lat numeric(25,18) NOT NULL,
    last_lng numeric(25,18) NOT NULL
);

--
-- PostgreSQL database dump complete
--


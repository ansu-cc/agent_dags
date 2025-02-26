--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5
-- Dumped by pg_dump version 10.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: order; Type: TABLE; Schema: webshop; Owner: postgres
--

CREATE TABLE webshop."order" (
    id integer NOT NULL,
    customerid integer,
    ordertimestamp timestamp with time zone DEFAULT now(),
    shippingaddressid integer,
    total money,
    shippingcost money,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone
);


ALTER TABLE webshop."order" OWNER TO postgres;

--
-- Name: TABLE "order"; Type: COMMENT; Schema: webshop; Owner: postgres
--

COMMENT ON TABLE webshop."order" IS 'Metadata for an order, see order_positions as well';


--
-- Name: order_id_seq; Type: SEQUENCE; Schema: webshop; Owner: postgres
--

CREATE SEQUENCE webshop.order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE webshop.order_id_seq OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: webshop; Owner: postgres
--

ALTER SEQUENCE webshop.order_id_seq OWNED BY webshop."order".id;


--
-- Name: order id; Type: DEFAULT; Schema: webshop; Owner: postgres
--

ALTER TABLE ONLY webshop."order" ALTER COLUMN id SET DEFAULT nextval('webshop.order_id_seq'::regclass);


--
-- Data for Name: order; Type: TABLE DATA; Schema: webshop; Owner: postgres
--

COPY webshop."order" (id, customerid, ordertimestamp, shippingaddressid, total, shippingcost, created, updated) FROM stdin;
11	229	2018-03-14 06:52:31.662986+01	229	$361.81	$3.90	2018-08-02 15:30:40.686986+02	\N
12	1077	2018-01-06 06:50:20.248586+01	1077	$341.57	$3.90	2018-08-02 15:30:40.686986+02	\N
13	865	2017-07-25 13:08:29.118986+02	865	$414.63	$3.90	2018-08-02 15:30:40.686986+02	\N
14	406	2017-11-12 12:01:20.402186+01	406	$344.80	$3.90	2018-08-02 15:30:40.686986+02	\N
15	757	2018-05-08 14:03:20.008586+02	757	$104.37	$3.90	2018-08-02 15:30:40.686986+02	\N
16	553	2017-08-23 17:25:14.670986+02	553	$264.10	$3.90	2018-08-02 15:30:40.686986+02	\N
17	345	2017-10-06 03:29:11.176586+02	345	$423.27	$3.90	2018-08-02 15:30:40.686986+02	\N
18	340	2017-01-27 23:39:04.917386+01	340	$373.80	$3.90	2018-08-02 15:30:40.686986+02	\N
19	273	2018-01-05 09:38:34.187786+01	273	$49.84	$3.90	2018-08-02 15:30:40.686986+02	\N
20	265	2018-03-13 23:14:51.237386+01	265	$458.74	$3.90	2018-08-02 15:30:40.686986+02	\N
21	1009	2018-01-17 20:34:44.507786+01	1009	$166.81	$3.90	2018-08-02 15:30:40.686986+02	\N
22	1072	2018-03-19 23:28:23.570186+01	1072	$127.00	$3.90	2018-08-02 15:30:40.686986+02	\N
23	1098	2017-08-16 09:09:58.686986+02	1098	$132.00	$3.90	2018-08-02 15:30:40.686986+02	\N
24	663	2017-02-14 10:26:10.830986+01	663	$237.36	$3.90	2018-08-02 15:30:40.686986+02	\N
25	1061	2016-09-07 20:04:02.171786+02	1061	$449.68	$3.90	2018-08-02 15:30:40.686986+02	\N
26	775	2017-10-23 10:51:54.078986+02	775	$153.33	$3.90	2018-08-02 15:30:40.686986+02	\N
27	1050	2017-02-23 11:03:12.174986+01	1050	$220.97	$3.90	2018-08-02 15:30:40.686986+02	\N
28	259	2017-11-10 13:04:23.944586+01	259	$382.37	$3.90	2018-08-02 15:30:40.686986+02	\N
29	189	2016-11-14 23:32:14.603786+01	189	$181.00	$3.90	2018-08-02 15:30:40.686986+02	\N
30	451	2017-04-12 19:55:42.088586+02	451	$113.00	$3.90	2018-08-02 15:30:40.686986+02	\N
\.


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: webshop; Owner: postgres
--

SELECT pg_catalog.setval('webshop.order_id_seq', 2010, true);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: webshop; Owner: postgres
--

ALTER TABLE ONLY webshop."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: order order_shippingaddressid_fkey; Type: FK CONSTRAINT; Schema: webshop; Owner: postgres
--

ALTER TABLE ONLY webshop."order"
    ADD CONSTRAINT order_shippingaddressid_fkey FOREIGN KEY (shippingaddressid) REFERENCES webshop.address(id);


--
-- PostgreSQL database dump complete
--

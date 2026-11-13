--
-- PostgreSQL database dump
--

\restrict P0Kxst8csaTeXKcV7HnrNb5pHRxjdYFQhnzHH9z8bhJjgu8NHTIvF3IFGjDuiCL

-- Dumped from database version 17.12
-- Dumped by pg_dump version 17.12

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
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    event character varying(50) NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    location character varying(200) NOT NULL
);


--
-- Name: participants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.participants (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    discipline character varying(50) NOT NULL,
    CONSTRAINT participants_name_check CHECK ((length(TRIM(BOTH FROM name)) > 0))
);


--
-- Name: participants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.participants ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.participants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.events (event, title, description, location) FROM stdin;
running	Бег на 3 километра	Соревнование по бегу на длинную дистанцию	Школьный стадион
pushups	Отжимания	Соревнование по отжиманиям	Спортивный зал
pullups	Подтягивания	Соревнование по подтягиваниям	Спортивный зал
flexibility	Гибкость	Соревнование по растяжке	Спортивный зал
jumps	Прыжки в длину	Соревнование по прыжкам	Школьный стадион
\.


--
-- Data for Name: participants; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.participants (id, name, discipline) FROM stdin;
1	Иванов Александр Сергеевич	running
3	Севрюков Александр Геннадьевич	pushups
4	Чикенбургеров Артём Сергеевич	flexibility
\.


--
-- Name: participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.participants_id_seq', 4, true);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event);


--
-- Name: participants participants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_pkey PRIMARY KEY (id);


--
-- Name: participants participants_discipline_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_discipline_fkey FOREIGN KEY (discipline) REFERENCES public.events(event);


--
-- PostgreSQL database dump complete
--

\unrestrict P0Kxst8csaTeXKcV7HnrNb5pHRxjdYFQhnzHH9z8bhJjgu8NHTIvF3IFGjDuiCL


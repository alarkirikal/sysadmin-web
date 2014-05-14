--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: students; Type: TABLE; Schema: public; Owner: sysadmin; Tablespace: 
--

CREATE TABLE students (
    id character varying,
    study_nr character varying,
    name character varying,
    lastname character varying,
    faculty character varying,
    year character varying,
    study_degree character varying,
    study_curriculum character varying,
    group_nr character varying,
    email_ut character varying,
    email_ext character varying,
    course_status character varying,
    course_time character varying,
    student_uid character varying,
    status_mail character varying,
    status_smime character varying,
    status_csr character varying,
    status_certsent character varying,
    username character varying
);


ALTER TABLE public.students OWNER TO sysadmin;

--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: sysadmin
--

COPY students (id, study_nr, name, lastname, faculty, year, study_degree, study_curriculum, group_nr, email_ut, email_ext, course_status, course_time, student_uid, status_mail, status_smime, status_csr, status_certsent, username) FROM stdin;
\.


--
-- Name: public; Type: ACL; Schema: -; Owner: alarkirikal
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM alarkirikal;
GRANT ALL ON SCHEMA public TO alarkirikal;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


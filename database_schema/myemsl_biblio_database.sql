--
-- Name: eus_new; Type: SCHEMA; Schema: -; Owner: metadata_admins
--

CREATE SCHEMA eus_new;


ALTER SCHEMA eus_new OWNER TO metadata_admins;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

--COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = eus_new, pg_catalog;

--
-- Name: update_modified_column(); Type: FUNCTION; Schema: eus_new; Owner: metadata_admins
--

CREATE FUNCTION update_modified_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
    NEW.updated = now();
    RETURN NEW;
END;$$;


ALTER FUNCTION eus_new.update_modified_column() OWNER TO metadata_admins;


--
-- Name: users; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE users (
    person_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    network_id character varying,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.users OWNER TO metadata_admins;

--
-- Name: institution_person_xref; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE institution_person_xref (
    person_id integer NOT NULL,
    institution_id integer NOT NULL,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.institution_person_xref OWNER TO metadata_admins;

--
-- Name: institutions; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE institutions (
    institution_id integer NOT NULL,
    institution_name text NOT NULL,
    association_cd character varying DEFAULT 'UNK'::character varying NOT NULL,
    is_foreign smallint DEFAULT 0 NOT NULL,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.institutions OWNER TO metadata_admins;

--
-- Name: instruments; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE instruments (
    instrument_id integer NOT NULL,
    display_name character varying,
    instrument_name character varying,
    name_short character varying,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.instruments OWNER TO metadata_admins;

--
-- Name: internal_publications; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

-- CREATE TABLE internal_publications (
--     eus_publication_id integer NOT NULL,
--     submitted_by integer NOT NULL,
--     submitted_date date,
--     document_url character varying,
--     file_size_in_bytes bigint,
--     citation_text text,
--     last_change_date timestamp(6) without time zone,
--     created timestamp(6) with time zone DEFAULT now() NOT NULL,
--     updated timestamp(6) with time zone NOT NULL,
--     deleted timestamp(6) with time zone
-- );


-- ALTER TABLE eus_new.internal_publications OWNER TO metadata_admins;

--
-- Name: journal_cache; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE journal_cache (
    journal_id integer NOT NULL,
    journal_name character varying NOT NULL,
    impact_factor real,
    website_url character varying
);


ALTER TABLE eus_new.journal_cache OWNER TO metadata_admins;

--
-- Name: proposal_info; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE proposal_info (
    proposal_id character varying NOT NULL,
    title text NOT NULL,
    abstract text,
    science_theme character varying,
    science_theme_id integer,
    proposal_type character varying,
    submitted_date date NOT NULL,
    accepted_date date NOT NULL,
    actual_start_date date,
    actual_end_date date,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.proposal_info OWNER TO metadata_admins;

--
-- Name: proposal_instrument_xref; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE proposal_instrument_xref (
    instrument_id integer NOT NULL,
    proposal_id character varying NOT NULL,
    hours_estimated integer NOT NULL,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    updated timestamp with time zone NOT NULL,
    deleted timestamp with time zone
);


ALTER TABLE eus_new.proposal_instrument_xref OWNER TO metadata_admins;


--
-- Name: proposal_participants; Type: TABLE; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE proposal_participants (
    proposal_id character varying NOT NULL,
    person_id integer NOT NULL,
    proposal_author_sw character varying DEFAULT false NOT NULL,
    proposal_co_author_sw character varying DEFAULT false NOT NULL,
    last_change_date timestamp(6) without time zone NOT NULL,
    created timestamp(6) with time zone DEFAULT now() NOT NULL,
    updated timestamp(6) with time zone NOT NULL,
    deleted timestamp(6) with time zone
);


ALTER TABLE eus_new.proposal_participants OWNER TO metadata_admins;


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (person_id);


--
-- Name: institution_person_xref_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY institution_person_xref
    ADD CONSTRAINT institution_person_xref_pkey PRIMARY KEY (person_id);


--
-- Name: institutions_new_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY institutions
    ADD CONSTRAINT institutions_new_pkey PRIMARY KEY (institution_id);


--
-- Name: instruments_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY instruments
    ADD CONSTRAINT instruments_pkey PRIMARY KEY (instrument_id);


--
-- Name: journal_cache_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY journal_cache
    ADD CONSTRAINT journal_cache_pkey PRIMARY KEY (journal_id);


--
-- Name: eus_new_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY proposal_info
    ADD CONSTRAINT proposal_info_pkey PRIMARY KEY (proposal_id);


--
-- Name: proposal_instrument_xref_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY proposal_instrument_xref
    ADD CONSTRAINT proposal_instrument_xref_pkey PRIMARY KEY (instrument_id, proposal_id);


--
-- Name: proposal_participants_pkey; Type: CONSTRAINT; Schema: eus_new; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY proposal_participants
    ADD CONSTRAINT proposal_participants_pkey PRIMARY KEY (proposal_id, person_id);


--
-- Name: inst_person_updated_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER inst_person_updated_modified BEFORE INSERT OR UPDATE ON institution_person_xref FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: inst_updated_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER inst_updated_modified BEFORE INSERT OR UPDATE ON instruments FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: institution_updated_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER institution_updated_modified BEFORE INSERT OR UPDATE ON institutions FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: prop_inst_updated_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER prop_inst_updated_modified BEFORE INSERT OR UPDATE ON proposal_instrument_xref FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: prop_part_updated_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER prop_part_updated_modified BEFORE INSERT OR UPDATE ON proposal_participants FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: trg_prop_info_update; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER trg_prop_info_update BEFORE INSERT OR UPDATE ON proposal_info FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: user_update_modified; Type: TRIGGER; Schema: eus_new; Owner: metadata_admins
--

CREATE TRIGGER user_update_modified BEFORE INSERT OR UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_modified_column();



--
-- Name: users; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE users FROM metadata_admins;
GRANT ALL ON TABLE users TO metadata_admins;
GRANT SELECT ON TABLE users TO metadata_readers;


--
-- Name: institution_person_xref; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE institution_person_xref FROM metadata_admins;
GRANT ALL ON TABLE institution_person_xref TO metadata_admins;
GRANT SELECT ON TABLE institution_person_xref TO metadata_readers;


--
-- Name: institutions; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE institutions FROM metadata_admins;
GRANT ALL ON TABLE institutions TO metadata_admins;
GRANT SELECT ON TABLE institutions TO metadata_readers;


--
-- Name: instruments; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE instruments FROM metadata_admins;
GRANT ALL ON TABLE instruments TO metadata_admins;
GRANT SELECT ON TABLE instruments TO metadata_readers;


--
-- Name: internal_publications; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

-- REVOKE ALL ON TABLE internal_publications FROM metadata_admins;
-- GRANT ALL ON TABLE internal_publications TO metadata_admins;
-- GRANT SELECT ON TABLE internal_publications TO metadata_readers;


--
-- Name: journal_cache; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE journal_cache FROM metadata_admins;
GRANT ALL ON TABLE journal_cache TO metadata_admins;
GRANT SELECT ON TABLE journal_cache TO metadata_readers;


--
-- Name: proposal_info; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE proposal_info FROM metadata_admins;
GRANT ALL ON TABLE proposal_info TO metadata_admins;
GRANT SELECT ON TABLE proposal_info TO metadata_readers;


--
-- Name: proposal_instrument_xref; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE proposal_instrument_xref FROM metadata_admins;
GRANT ALL ON TABLE proposal_instrument_xref TO metadata_admins;
GRANT SELECT ON TABLE proposal_instrument_xref TO metadata_readers;


--
-- Name: proposal_int_publication_xref; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

-- REVOKE ALL ON TABLE proposal_int_publication_xref FROM metadata_admins;
-- GRANT ALL ON TABLE proposal_int_publication_xref TO metadata_admins;
-- GRANT SELECT ON TABLE proposal_int_publication_xref TO metadata_readers;


--
-- Name: proposal_participants; Type: ACL; Schema: eus_new; Owner: metadata_admins
--

REVOKE ALL ON TABLE proposal_participants FROM metadata_admins;
GRANT ALL ON TABLE proposal_participants TO metadata_admins;
GRANT SELECT ON TABLE proposal_participants TO metadata_readers;


--
-- PostgreSQL database dump complete
--


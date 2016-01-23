--
-- Name: erica_info; Type: SCHEMA; Schema: -; Owner: metadata_admins
--

CREATE SCHEMA erica_info;


ALTER SCHEMA erica_info OWNER TO metadata_admins;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = erica_info, pg_catalog;

--
-- Name: update_modified_column(); Type: FUNCTION; Schema: erica_info; Owner: metadata_admins
--

CREATE FUNCTION update_modified_column() RETURNS trigger
		LANGUAGE plpgsql
		AS $$BEGIN
		NEW.updated = now();
		RETURN NEW;
END;$$;


ALTER FUNCTION erica_info.update_modified_column() OWNER TO metadata_admins;




--
-- Name: citations; Type: TABLE; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE citations (
		product_id integer NOT NULL,
		article_title text NOT NULL,
		journal_id integer NOT NULL,
		journal_volume integer NOT NULL,
		journal_issue integer,
		page_range character varying,
		abstract_text text,
		xml_text text,
		pnnl_clearance_id character varying,
		doi_reference character varying,
		last_change_date timestamp(6) without time zone NOT NULL,
		created timestamp(6) with time zone DEFAULT now() NOT NULL,
		updated timestamp(6) with time zone NOT NULL,
		deleted timestamp(6) with time zone
);


ALTER TABLE erica_info.citations OWNER TO metadata_admins;

--
-- Name: contributors; Type: TABLE; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE contributors (
		author_id integer NOT NULL,
		first_name character varying NOT NULL,
		middle_initial character varying,
		last_name character varying NOT NULL,
		network_id character varying,
		dept_code character varying,
		institution_name text,
		last_change_date timestamp(6) without time zone NOT NULL,
		created timestamp(6) with time zone DEFAULT now() NOT NULL,
		updated timestamp(6) with time zone NOT NULL,
		deleted timestamp(6) with time zone
);


ALTER TABLE erica_info.contributors OWNER TO metadata_admins;

--
-- Name: keywords; Type: TABLE; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE keywords (
		keyword_id integer NOT NULL,
		product_id integer NOT NULL,
		keyword character varying NOT NULL,
		last_change_date timestamp(6) without time zone NOT NULL,
		created timestamp(6) with time zone DEFAULT now() NOT NULL,
		updated timestamp(6) with time zone NOT NULL,
		deleted timestamp(6) with time zone
);


ALTER TABLE erica_info.keywords OWNER TO metadata_admins;

--
-- Name: product_contributor_xref; Type: TABLE; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

CREATE TABLE product_contributor_xref (
		product_id integer NOT NULL,
		author_id integer NOT NULL,
		author_precedence integer DEFAULT 1 NOT NULL,
		last_change_date timestamp(6) without time zone NOT NULL,
		created timestamp(6) with time zone DEFAULT now() NOT NULL,
		updated timestamp(6) with time zone NOT NULL,
		deleted timestamp(6) with time zone
);


ALTER TABLE erica_info.product_contributor_xref OWNER TO metadata_admins;


--
-- Name: citations_pkey; Type: CONSTRAINT; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY citations
		ADD CONSTRAINT citations_pkey PRIMARY KEY (product_id);


--
-- Name: contributors_pkey; Type: CONSTRAINT; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY contributors
		ADD CONSTRAINT contributors_pkey PRIMARY KEY (author_id);


--
-- Name: keywords_pkey; Type: CONSTRAINT; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY keywords
		ADD CONSTRAINT keywords_pkey PRIMARY KEY (keyword_id);


--
-- Name: product_contributor_xref_pkey; Type: CONSTRAINT; Schema: erica_info; Owner: metadata_admins; Tablespace: 
--

ALTER TABLE ONLY product_contributor_xref
		ADD CONSTRAINT product_contributor_xref_pkey PRIMARY KEY (product_id, author_id);


--
-- Name: cit_updated_modified; Type: TRIGGER; Schema: erica_info; Owner: metadata_admins
--

CREATE TRIGGER cit_updated_modified BEFORE INSERT OR UPDATE ON citations FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: contrib_updated_modified; Type: TRIGGER; Schema: erica_info; Owner: metadata_admins
--

CREATE TRIGGER contrib_updated_modified BEFORE INSERT OR UPDATE ON contributors FOR EACH ROW EXECUTE PROCEDURE update_modified_column();


--
-- Name: interal_pub_updated_modified; Type: TRIGGER; Schema: erica_info; Owner: metadata_admins
--

-- CREATE TRIGGER interal_pub_updated_modified BEFORE INSERT OR UPDATE ON internal_publications FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

--
-- Name: prod_contrib_updated_modified; Type: TRIGGER; Schema: erica_info; Owner: metadata_admins
--

CREATE TRIGGER prod_contrib_updated_modified BEFORE INSERT OR UPDATE ON product_contributor_xref FOR EACH ROW EXECUTE PROCEDURE update_modified_column();



--
-- Name: citations; Type: ACL; Schema: erica_info; Owner: metadata_admins
--

REVOKE ALL ON TABLE citations FROM PUBLIC;
REVOKE ALL ON TABLE citations FROM metadata_admins;
GRANT ALL ON TABLE citations TO metadata_admins;
GRANT SELECT ON TABLE citations TO metadata_readers;


--
-- Name: contributors; Type: ACL; Schema: erica_info; Owner: metadata_admins
--

REVOKE ALL ON TABLE contributors FROM PUBLIC;
REVOKE ALL ON TABLE contributors FROM metadata_admins;
GRANT ALL ON TABLE contributors TO metadata_admins;
GRANT SELECT ON TABLE contributors TO metadata_readers;


--
-- Name: keywords; Type: ACL; Schema: erica_info; Owner: metadata_admins
--

REVOKE ALL ON TABLE keywords FROM PUBLIC;
REVOKE ALL ON TABLE keywords FROM metadata_admins;
GRANT ALL ON TABLE keywords TO metadata_admins;
GRANT SELECT ON TABLE keywords TO metadata_readers;


--
-- Name: product_contributor_xref; Type: ACL; Schema: erica_info; Owner: metadata_admins
--

REVOKE ALL ON TABLE product_contributor_xref FROM PUBLIC;
REVOKE ALL ON TABLE product_contributor_xref FROM metadata_admins;
GRANT ALL ON TABLE product_contributor_xref TO metadata_admins;
GRANT SELECT ON TABLE product_contributor_xref TO metadata_readers;


--
-- Name: proposal_xref; Type: ACL; Schema: erica_info; Owner: metadata_admins
--

REVOKE ALL ON TABLE proposal_xref FROM PUBLIC;
REVOKE ALL ON TABLE proposal_xref FROM metadata_admins;
GRANT ALL ON TABLE proposal_xref TO metadata_admins;
GRANT SELECT ON TABLE proposal_xref TO metadata_readers;


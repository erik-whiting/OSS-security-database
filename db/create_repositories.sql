CREATE TABLE IF NOT EXISTS public.repositories
(
	id bigint NOT NULL,
	name character varying(150),
	html_url character varying(200),
	clone_url character varying(200),
	ssh_url character varying(200),
	git_url character varying(200),
	topics  character varying(400),
	stars bigint,
	forks bigint,
	watchers bigint,
	programming_language_id bigint,
	
	CONSTRAINT repositories_pkey PRIMARY KEY (id),
	CONSTRAINT programming_languages_fkey FOREIGN KEY (programming_language_id) REFERENCES programming_languages(id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repositories
	OWNER TO postgres

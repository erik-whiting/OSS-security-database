CREATE TABLE IF NOT EXISTS public.repositories
(
	id bigint NOT NULL,
	name character varying(150),
  description character varying(400),
  latest_recorded_commit character varying(40),
	html_url character varying(200),
	clone_url character varying(200),
	ssh_url character varying(200),
	git_url character varying(200),
	topics  character varying(400),
	stars bigint,
	forks bigint,
	watchers bigint,
  issues bigint,
	programming_language character varying(20),
  created date,
	
	CONSTRAINT repositories_pkey PRIMARY KEY (id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repositories
	OWNER TO postgres

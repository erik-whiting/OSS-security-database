CREATE TABLE IF NOT EXISTS public.repositories
(
	id bigint NOT NULL,
	name CHARACTER varying(400),
  description CHARACTER TEXT,
	html_url CHARACTER varying(450),
	clone_url CHARACTER varying(450),
	ssh_url CHARACTER varying(450),
	git_url CHARACTER varying(450),
	topics  CHARACTER TEXT,
	stars bigint,
	forks bigint,
	watchers bigint,
  issues bigint,
	programming_language CHARACTER varying(20),
  created date,

	CONSTRAINT repositories_pkey PRIMARY KEY (id)
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repositories
	OWNER TO postgres

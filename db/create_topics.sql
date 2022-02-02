CREATE TABLE IF NOT EXISTS public.topics
(
	id serial primary key,
	name character varying(400),
  occurences bigint
)
WITH (
	OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.topics
	OWNER TO postgres

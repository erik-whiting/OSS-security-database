CREATE TABLE IF NOT EXISTS public.analyses
(
  id SERIAL PRIMARY KEY,
  date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  repo_extraction_sql CHARACTER VARYING(1000),
  hash_of_codeql_repo CHARACTER VARYING(40),
  codeql_version CHARACTER VARYING(20),
  completed BOOLEAN DEFAULT false
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.analyses OWNER TO postgres
CREATE TABLE IF NOT EXISTS public.repo_topics
(
  id SERIAL PRIMARY KEY,
  repository_id BIGINT NOT NULL,
  topic CHARACTER VARYING(40),
  CONSTRAINT fk_repository FOREIGN KEY (repository_id) REFERENCES repositories(id)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.repo_topics OWNER TO postgres
CREATE TABLE IF NOT EXISTS public.repo_topics
(
  id SERIAL PRIMARY KEY,
  repository_id BIGINT NOT NULL,
  topic_id BIGINT NOT NULL,
  CONSTRAINT fk_repository FOREIGN KEY (repository_id) REFERENCES repositories(id),
  CONSTRAINT fk_topics FOREIGN KEY (topic_id) REFERENCES topics(id)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default

ALTER TABLE public.repo_topics OWNER TO postgres
CREATE TABLE IF NOT EXISTS public.analysis_repo
(
  id SERIAL PRIMARY KEY,
  analysis_id BIGINT NOT NULL,
  repository_id BIGINT NOT NULL,
  completed BOOLEAN DEFAULT false,
  CONSTRAINT fk_analysis_repo FOREIGN KEY (analysis_id) REFERENCES analyses(id),
  CONSTRAINT fk_repo_analysis FOREIGN KEY (repository_id) REFERENCES repositories(id)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.analysis_repo OWNER TO postgres
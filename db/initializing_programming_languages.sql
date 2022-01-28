-- Table: public.programming_languages

-- DROP TABLE public.programming_languages;

CREATE TABLE IF NOT EXISTS public.programming_languages
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 1000 CACHE 1 ),
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    compiled boolean,
    CONSTRAINT programming_languages_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.programming_languages
    OWNER to postgres;

INSERT INTO programming_languages
  (name, compiled)
  VALUES
  ('c', true),
  ('c++', true),
  ('c#', true),
  ('go', true),
  ('java', true),
  ('javascript', false),
  ('python', false),
  ('typescript', false);

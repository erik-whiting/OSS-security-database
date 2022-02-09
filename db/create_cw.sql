CREATE TABLE IF NOT EXISTS public.common_weakness_enumerations
(
  id INT NOT NULL,
  name CHARACTER VARYING(150),
  abstraction CHARACTER VARYING(10),
  structure CHARACTER VARYING(15),
  status CHARACTER VARYING(15)
)
WITH (
  OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.common_weakness_enumerations OWNER TO postgres

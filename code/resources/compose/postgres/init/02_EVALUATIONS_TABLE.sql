CREATE TABLE IF NOT EXISTS avh_evalscore_v1.evaluations (
    id          uuid            NOT NULL,
    name        varchar(255)    NOT NULL,
    description text            NULL,
    target      jsonb           NOT NULL,
    evaluator   jsonb           NOT NULL,
    repetitions integer         NOT NULL,
    concurrency integer         NOT NULL,
    created_at  timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT evaluations_pkey PRIMARY KEY (id),
    CONSTRAINT ck_evaluations_repetitions CHECK (repetitions BETWEEN 1 AND 100),
    CONSTRAINT ck_evaluations_concurrency CHECK (concurrency BETWEEN 1 AND 20)
);

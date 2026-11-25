CREATE TABLE IF NOT EXISTS avh_evalscore_v1.evaluation_cases (
    id              uuid            NOT NULL,
    evaluation_id   uuid            NOT NULL,
    kind            varchar(32)     NOT NULL,
    input           text            NULL,
    messages        jsonb           NOT NULL DEFAULT '[]'::jsonb,
    expected_output text            NULL,
    trajectory      jsonb           NULL,
    created_at      timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT evaluation_cases_pkey PRIMARY KEY (id),
    CONSTRAINT fk_evaluation_cases_evaluation
        FOREIGN KEY (evaluation_id)
        REFERENCES avh_evalscore_v1.evaluations (id)
        ON DELETE CASCADE,
    CONSTRAINT ck_evaluation_cases_kind
        CHECK (kind IN ('SINGLE_TURN', 'MULTI_TURN', 'TRAJECTORY'))
);

CREATE INDEX IF NOT EXISTS ix_evaluation_cases_evaluation_id
    ON avh_evalscore_v1.evaluation_cases (evaluation_id);

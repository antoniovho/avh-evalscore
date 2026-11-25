CREATE TABLE IF NOT EXISTS avh_evalscore_v1.evaluation_runs (
    id            uuid            NOT NULL,
    evaluation_id uuid            NOT NULL,
    snapshot      jsonb           NOT NULL,
    status        varchar(32)     NOT NULL,
    created_at    timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at    timestamptz(6)  NULL,
    finished_at   timestamptz(6)  NULL,
    error         text            NULL,
    updated_at    timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT evaluation_runs_pkey PRIMARY KEY (id),
    CONSTRAINT fk_evaluation_runs_evaluation
        FOREIGN KEY (evaluation_id)
        REFERENCES avh_evalscore_v1.evaluations (id)
        ON DELETE RESTRICT,
    CONSTRAINT ck_evaluation_runs_status
        CHECK (status IN ('CREATED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'))
);

CREATE INDEX IF NOT EXISTS ix_evaluation_runs_evaluation_id
    ON avh_evalscore_v1.evaluation_runs (evaluation_id);
CREATE INDEX IF NOT EXISTS ix_evaluation_runs_status
    ON avh_evalscore_v1.evaluation_runs (status);
CREATE INDEX IF NOT EXISTS idx_evaluation_runs_status_created_at
    ON avh_evalscore_v1.evaluation_runs (status, created_at);

CREATE TABLE IF NOT EXISTS avh_evalscore_v1.evaluation_results (
    id               uuid            NOT NULL,
    run_id           uuid            NOT NULL,
    case_id          uuid            NOT NULL,
    attempt          integer         NOT NULL,
    output           text            NULL,
    score            double precision NOT NULL,
    passed           boolean         NOT NULL,
    reasoning        text            NOT NULL,
    trace            jsonb           NULL,
    judge_trace      jsonb           NULL,
    trajectory_check jsonb           NULL,
    created_at       timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       timestamptz(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT evaluation_results_pkey PRIMARY KEY (id),
    CONSTRAINT fk_evaluation_results_run
        FOREIGN KEY (run_id)
        REFERENCES avh_evalscore_v1.evaluation_runs (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_evaluation_results_case
        FOREIGN KEY (case_id)
        REFERENCES avh_evalscore_v1.evaluation_cases (id)
        ON DELETE RESTRICT,
    CONSTRAINT uq_evaluation_results_run_case_attempt UNIQUE (run_id, case_id, attempt),
    CONSTRAINT ck_evaluation_results_attempt CHECK (attempt >= 1),
    CONSTRAINT ck_evaluation_results_score CHECK (score BETWEEN 0 AND 1)
);

CREATE INDEX IF NOT EXISTS ix_evaluation_results_run_id
    ON avh_evalscore_v1.evaluation_results (run_id);
CREATE INDEX IF NOT EXISTS ix_evaluation_results_case_id
    ON avh_evalscore_v1.evaluation_results (case_id);

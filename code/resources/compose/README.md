# AVH Evalscore PostgreSQL Development Environment

This Compose package runs the PostgreSQL database required by Evalscore in a
local development environment. It is intentionally a clean initial setup: the
database has not been deployed yet, so its schema is created from the ordered
SQL scripts under `postgres/init/`.

## Start the database

From this directory:

```bash
docker compose up -d
docker compose ps
```

PostgreSQL is available at `localhost:55435` by default.

| Setting | Value |
| --- | --- |
| Database | `evalscore` |
| User | `postgresqldba` |
| Password | `admin` |
| Application schema | `avh_evalscore_v1` |

The host port can be changed without editing the Compose file:

```bash
POSTGRES_PORT=55436 docker compose up -d
```

Configure the application local environment with the same connection values:

```dotenv
DATABASE_HOST=localhost
DATABASE_PORT=55435
DATABASE_NAME=evalscore
DATABASE_USER=postgresqldba
DATABASE_PASSWORD=admin
```

You can verify the initialized tables with:

```bash
docker compose exec postgres psql -U postgresqldba -d evalscore \
  -c '\\dt avh_evalscore_v1.*'
```

## Schema initialization and reset

The official PostgreSQL image executes the files mounted in
`/docker-entrypoint-initdb.d` only when the named `postgres-data` volume is
created for the first time. They run in lexical order:

1. `01_CREATE_SCHEMA.sql`
2. `02_EVALUATIONS_TABLE.sql`
3. `03_EVALUATION_CASES_TABLE.sql`
4. `04_EVALUATION_RUNS_TABLE.sql`
5. `05_EVALUATION_RESULTS_TABLE.sql`

To discard local data and recreate the database from those scripts:

```bash
docker compose down --volumes
docker compose up -d
```

There are deliberately no historical migrations in this first-release setup.
Once a database has been deployed, schema changes must be introduced as
forward-only, versioned SQL migrations; do not modify an initialization script
that may already have been used to create a database.

## Production note

The credentials above are for local development only. Deployments must provide
their database endpoint and credentials through the platform secret mechanism,
never through this Compose file.

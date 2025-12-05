## Food Tracker

This is a FastAPI backend that combines LangChain Agents, Supabase, and pgvector to deliver an AI-powered food tracking system. The API supports natural-language queries, vector search, and tool calling agents to retrieve meals, symptoms, and user-specific data.

It uses an Agentic RAG pipeline to ground responses on user-uploaded documents stored in Supabase.

Features:

- FastAPI backend with clean modular architecture
- LangChain agent with custom tools
- Supabase pgvecytor for document embeddings and semantic search
- Agentic RAG ( tool invocation + retrieval )
- Authentication and per-user data isolation
- SQLAlchemy models + Pydantic schemas

### Supabase schema

```sql

CREATE TABLE public.document (
  id bigint NOT NULL DEFAULT nextval('documents_id_seq'::regclass),
  content text,
  embedding USER-DEFINED,
  meta jsonb,
  filename text,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT document_pkey PRIMARY KEY (id)
);
CREATE TABLE public.food (
  id integer NOT NULL DEFAULT nextval('food_id_seq'::regclass),
  created_at timestamp without time zone NOT NULL DEFAULT now(),
  name character varying,
  category character varying,
  histamine_level character varying,
  notes character varying,
  CONSTRAINT food_pkey PRIMARY KEY (id)
);
CREATE TABLE public.meal (
  id integer NOT NULL DEFAULT nextval('meal_id_seq'::regclass),
  created_at timestamp without time zone NOT NULL DEFAULT now(),
  user_id bigint,
  name text NOT NULL,
  CONSTRAINT meal_pkey PRIMARY KEY (id)
);
CREATE TABLE public.meal_food (
  meal_id integer NOT NULL,
  food_id integer NOT NULL,
  CONSTRAINT meal_food_pkey PRIMARY KEY (food_id, meal_id)
);
CREATE TABLE public.symptom (
  id integer NOT NULL DEFAULT nextval('symptom_id_seq'::regclass),
  created_at timestamp without time zone NOT NULL DEFAULT now(),
  user_id bigint,
  datetime timestamp without time zone,
  symptom_type character varying,
  severity character varying,
  notes character varying,
  meal_id integer,
  CONSTRAINT symptom_pkey PRIMARY KEY (id)
);
CREATE TABLE public.user (
  id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  created_at timestamp without time zone NOT NULL DEFAULT now(),
  username character varying,
  password character varying,
  name character varying,
  lastname character varying,
  email character varying,
  CONSTRAINT user_pkey PRIMARY KEY (id)
);
```

### Deployment

You can deploy it to railway by conteinerizing the application, pushing it to dockerhub and then pulling it from there.

```shell
docker buildx build --platform linux/amd64,linux/arm64 -t username/food-tracker:v1.0 --push .
```

### How to run it locally ?

Clone the repository

```shell
git clone food-tracker-api
```

Create a virtual environment

```shell
python3 -m venv food-tracker-env
```

Activate it

```shell
source food-tracker-env/bin/activate
```

Install your exact dependencies

```shell
pip install -r requirements.txt
```

Run it

```shell
fastapi dev main.py
```

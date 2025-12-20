-- food --

create table public.food (
  id serial not null,
  created_at timestamp without time zone not null default now(),
  name character varying(255) null,
  category character varying(255) null,
  histamine_level character varying(255) null,
  notes character varying(255) null,
  constraint food_pkey primary key (id)
) TABLESPACE pg_default;

-- meal --

create table public.meal (
  id serial not null,
  created_at timestamp without time zone not null default now(),
  name text not null,
  user_id uuid null,
  constraint meal_pkey primary key (id),
  constraint meal_user_id_fkey foreign KEY (user_id) references auth.users (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;

-- meal_food --

create table public.meal_food (
  meal_id integer not null,
  food_id integer not null,
  constraint meal_food_pkey primary key (meal_id, food_id),
  constraint meal_food_food_id_fkey foreign KEY (food_id) references food (id) on update CASCADE on delete CASCADE,
  constraint meal_food_meal_id_fkey foreign KEY (meal_id) references meal (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;

-- symptom --

create table public.symptom (
  id serial not null,
  created_at timestamp without time zone not null default now(),
  datetime timestamp without time zone null,
  symptom_type character varying(255) null,
  severity character varying(255) null,
  notes text null,
  meal_id integer null,
  user_id uuid null,
  constraint symptoms_pkey primary key (id),
  constraint symptom_meal_id_fkey foreign KEY (meal_id) references meal (id) on update CASCADE on delete CASCADE,
  constraint symptom_user_id_fkey foreign KEY (user_id) references auth.users (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;

-- document --

create table public.document (
  id bigserial not null,
  content text null,
  embedding public.vector null,
  meta jsonb null,
  filename text null,
  created_at timestamp without time zone null default now(),
  constraint documents_pkey primary key (id)
) TABLESPACE pg_default;

-- email_jobs --

create table public.email_jobs (
  id uuid not null default gen_random_uuid (),
  idempotency_key text null,
  user_id uuid not null,
  period text not null,
  payload jsonb not null,
  status text not null,
  attempts integer not null default 0,
  last_error text null,
  created_at timestamp with time zone null default now(),
  updated_at timestamp with time zone null default now(),
  constraint email_jobs_pkey primary key (id),
  constraint email_jobs_idempotency_key_key unique (idempotency_key)
) TABLESPACE pg_default;
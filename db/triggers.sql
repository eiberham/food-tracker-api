-- email sendout --

create or replace function enqueue_email_job()
returns trigger as $$
begin
  perform pgmq.send(
    'email_jobs'::text,
    json_build_object('email_job_id', new.id)::jsonb
  );

  return new;
end;
$$ language plpgsql;

create trigger email_job_enqueue 
after insert on email_job
for each row execute function enqueue_email_job();

-- wrapper function to make pgmq_read work --

CREATE OR REPLACE FUNCTION public.pgmq_read(
    queue_name text,
    vt integer,
    qty integer,
    conditional jsonb DEFAULT '{}'
)
RETURNS TABLE (
    msg_id bigint,
    read_ct integer,
    enqueued_at timestamptz,
    vt timestamptz,
    message jsonb
)
LANGUAGE SQL
AS $$
    SELECT
        msg_id,
        read_ct,
        enqueued_at,
        vt,
        message
    FROM pgmq.read(queue_name, vt, qty, conditional);
$$;

-- wrapper function to make pgmq_delete work --

CREATE OR REPLACE FUNCTION public.pgmq_delete(
  queue_name text,
  msg_id bigint
)
RETURNS void
LANGUAGE SQL
AS $$
  SELECT pgmq.delete(queue_name, msg_id);
$$;
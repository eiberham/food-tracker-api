CREATE OR REPLACE FUNCTION public.match_embeddings(query_embedding vector, match_count integer DEFAULT 5)
 RETURNS TABLE(id bigint, content text, meta jsonb, similarity double precision)
 LANGUAGE sql
 STABLE PARALLEL SAFE
AS $function$
    SELECT
        d.id,
        d.content,
        d.meta,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM public.document d
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
$function$
;
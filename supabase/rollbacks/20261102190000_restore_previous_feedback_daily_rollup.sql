-- Rollback for 20261102190000_fix_feedback_daily_rollup.sql.
-- Restores the previous function body if an operator explicitly decides to revert.
CREATE OR REPLACE FUNCTION ima_internal.refresh_feedback_daily_rollup()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO ''
AS $function$
DECLARE d date := (now() AT TIME ZONE 'utc')::date;
BEGIN
  INSERT INTO public.feedback_daily_rollup(
    rollup_date, received_count, candidate_count, high_priority_count, categories, generated_at
  )
  SELECT d,
    count(*) FILTER (WHERE fa.date_utc = d),
    count(*) FILTER (WHERE fl.status = 'candidate' AND fa.date_utc = d),
    count(*) FILTER (WHERE fl.priority = 'high' AND fa.date_utc = d),
    COALESCE(jsonb_object_agg(COALESCE(fl.category, 'unclassified'), cnt) FILTER (WHERE cat_ok), '{}'::jsonb),
    now()
  FROM public.feedback_archive AS fa
  LEFT JOIN public.feedback_learning AS fl ON fl.feedback_id = fa.id
  LEFT JOIN LATERAL (
    SELECT COALESCE(fl2.category, 'unclassified') AS cat, count(*) AS cnt, true AS cat_ok
    FROM public.feedback_archive AS fa2
    LEFT JOIN public.feedback_learning AS fl2 ON fl2.feedback_id = fa2.id
    WHERE fa2.date_utc = d
    GROUP BY COALESCE(fl2.category, 'unclassified')
  ) AS x ON true
  WHERE fa.date_utc = d
  GROUP BY d
  ON CONFLICT (rollup_date) DO UPDATE SET
    received_count = EXCLUDED.received_count,
    candidate_count = EXCLUDED.candidate_count,
    high_priority_count = EXCLUDED.high_priority_count,
    categories = EXCLUDED.categories,
    generated_at = now();
END;
$function$;

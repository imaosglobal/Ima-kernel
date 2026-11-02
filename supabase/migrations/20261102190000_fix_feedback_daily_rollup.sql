-- Rebuild completed UTC-day feedback rollups.
-- The previous function used today's UTC date at 00:05 UTC, when the day had
-- just begun, so it skipped the feedback submitted during the previous day.
-- This version refreshes every completed day and uses DISTINCT IDs to avoid
-- count inflation from joins.

CREATE OR REPLACE FUNCTION ima_internal.refresh_feedback_daily_rollup()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO ''
AS $function$
DECLARE
  d date;
BEGIN
  FOR d IN
    SELECT DISTINCT fa.date_utc
    FROM public.feedback_archive AS fa
    WHERE fa.date_utc < (now() AT TIME ZONE 'utc')::date
    ORDER BY fa.date_utc
  LOOP
    WITH daily AS (
      SELECT
        fa.date_utc,
        count(DISTINCT fa.id)::integer AS received_count,
        (count(DISTINCT fa.id) FILTER (WHERE fl.status = 'candidate'))::integer AS candidate_count,
        (count(DISTINCT fa.id) FILTER (WHERE fl.priority = 'high'))::integer AS high_priority_count
      FROM public.feedback_archive AS fa
      LEFT JOIN public.feedback_learning AS fl
        ON fl.feedback_id = fa.id
      WHERE fa.date_utc = d
      GROUP BY fa.date_utc
    ),
    category_counts AS (
      SELECT
        fa.date_utc,
        COALESCE(fl.category, 'unclassified') AS category,
        count(DISTINCT fa.id)::integer AS category_count
      FROM public.feedback_archive AS fa
      LEFT JOIN public.feedback_learning AS fl
        ON fl.feedback_id = fa.id
      WHERE fa.date_utc = d
      GROUP BY fa.date_utc, COALESCE(fl.category, 'unclassified')
    ),
    categories AS (
      SELECT
        cc.date_utc,
        jsonb_object_agg(cc.category, cc.category_count) AS categories
      FROM category_counts AS cc
      GROUP BY cc.date_utc
    )
    INSERT INTO public.feedback_daily_rollup (
      rollup_date,
      received_count,
      candidate_count,
      high_priority_count,
      categories,
      generated_at
    )
    SELECT
      daily.date_utc,
      daily.received_count,
      daily.candidate_count,
      daily.high_priority_count,
      COALESCE(categories.categories, '{}'::jsonb),
      now()
    FROM daily
    LEFT JOIN categories USING (date_utc)
    ON CONFLICT (rollup_date) DO UPDATE SET
      received_count = EXCLUDED.received_count,
      candidate_count = EXCLUDED.candidate_count,
      high_priority_count = EXCLUDED.high_priority_count,
      categories = EXCLUDED.categories,
      generated_at = now();
  END LOOP;
END;
$function$;

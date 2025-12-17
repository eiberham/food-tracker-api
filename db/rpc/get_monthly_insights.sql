CREATE OR REPLACE FUNCTION get_monthly_insights(
    p_user_id UUID
)
RETURNS TABLE(
    meal_id INTEGER,
    meal_datetime TIMESTAMP,
    meal_description TEXT,
    symptom_id INTEGER,
    symptom_datetime TIMESTAMP,
    symptom_type VARCHAR(255),
    symptom_severity VARCHAR(255),
    symptom_notes TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id AS meal_id,
        m.created_at AS meal_datetime,
        m.name AS meal_description,
        s.id AS symptom_id,
        s.created_at AS symptom_datetime,
        s.symptom_type,
        s.severity AS symptom_severity,
        s.notes AS symptom_notes
    FROM meal m
    LEFT JOIN symptom s ON m.user_id = s.user_id
        AND DATE_TRUNC('month', m.created_at) = DATE_TRUNC('month', s.created_at)
    WHERE m.user_id = p_user_id
      AND m.created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
      AND m.created_at < DATE_TRUNC('month', CURRENT_DATE);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
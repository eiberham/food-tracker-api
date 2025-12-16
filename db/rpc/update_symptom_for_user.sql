CREATE OR REPLACE FUNCTION update_symptom_for_user(
    p_symptom_id INTEGER,
    p_datetime TIMESTAMP,
    p_meal_id INTEGER,
    p_notes TEXT,
    p_severity TEXT,
    p_symptom_type TEXT
)
RETURNS TABLE(
    id INTEGER,
    datetime TIMESTAMP,
    symptom_type VARCHAR(255),
    severity VARCHAR(255), 
    notes TEXT,
    meal_id INTEGER,
    user_id UUID,
    created_at TIMESTAMP
) AS $$
DECLARE
    current_user_id UUID;
BEGIN
    current_user_id := auth.uid();
    
    -- Update the symptom
    UPDATE symptom
    SET datetime = p_datetime,
        symptom_type = p_symptom_type,
        severity = p_severity,
        notes = p_notes,
        meal_id = p_meal_id
    WHERE symptom.id = p_symptom_id AND symptom.user_id = current_user_id;
    
    -- Return the symptom
    RETURN QUERY
    SELECT s.id, s.datetime, s.symptom_type, s.severity, s.notes, s.meal_id, s.user_id, s.created_at
    FROM symptom s
    WHERE s.id = p_symptom_id AND s.user_id = current_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
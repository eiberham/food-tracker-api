CREATE OR REPLACE FUNCTION create_symptom_for_user(
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
    new_symptom_id INTEGER;
    current_user_id UUID;
BEGIN
    current_user_id := auth.uid();
    
    -- Create the symptom
    INSERT INTO symptom (datetime, symptom_type, severity, notes, meal_id, user_id)
    VALUES (p_datetime, p_symptom_type, p_severity, p_notes, p_meal_id, current_user_id)
    RETURNING symptom.id INTO new_symptom_id;
    
    -- Return the symptom
    RETURN QUERY
    SELECT s.id, s.datetime, s.symptom_type, s.severity, s.notes, s.meal_id, s.user_id, s.created_at
    FROM symptom s
    WHERE s.id = new_symptom_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
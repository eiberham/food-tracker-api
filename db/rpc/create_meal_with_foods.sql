CREATE OR REPLACE FUNCTION create_meal_with_foods(
    meal_name TEXT,
    food_ids INTEGER[]
)
RETURNS TABLE(
    id INTEGER,
    name TEXT,
    user_id UUID,
    created_at TIMESTAMP
) AS $$
DECLARE
    new_meal_id INTEGER;
    food_id INTEGER;
    current_user_id UUID;
BEGIN
    current_user_id := auth.uid();
    
    -- Create the meal
    INSERT INTO meal (name, user_id)
    VALUES (meal_name, current_user_id)
    RETURNING meal.id INTO new_meal_id;
    
    -- Insert meal_foods
    IF array_length(food_ids, 1) > 0 THEN
        FOREACH food_id IN ARRAY food_ids
        LOOP
            BEGIN
                INSERT INTO meal_food (meal_id, food_id) 
                VALUES (new_meal_id, food_id);
            END;
        END LOOP;
    END IF;
    
    -- Return the created meal
    RETURN QUERY
    SELECT m.id, m.name, m.user_id, m.created_at
    FROM meal m
    WHERE m.id = new_meal_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
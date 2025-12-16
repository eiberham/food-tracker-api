CREATE OR REPLACE FUNCTION update_meal_with_foods(
  p_meal_id INTEGER,
  meal_name TEXT DEFAULT NULL,
  food_ids INTEGER[] DEFAULT NULL
)
RETURNS TABLE(id INTEGER, name TEXT, user_id UUID, created_at TIMESTAMP)
LANGUAGE plpgsql
AS $$
DECLARE
  food_id INTEGER;
BEGIN
  -- Update meal basic info (if provided)
  IF meal_name IS NOT NULL THEN
    UPDATE meal 
    SET name = meal_name 
    WHERE meal.id = p_meal_id;
  END IF;
  
  -- Handle food associations (if provided)
  IF food_ids IS NOT NULL THEN
    DELETE FROM meal_food WHERE meal_id = p_meal_id;
    
    IF array_length(food_ids, 1) > 0 THEN
      FOREACH food_id IN ARRAY food_ids
      LOOP
        INSERT INTO meal_food (meal_id, food_id) 
        VALUES (p_meal_id, food_id);
      END LOOP;
    END IF;
  END IF;
  
  -- Return updated meal
  RETURN QUERY 
  SELECT m.id, m.name, m.user_id, m.created_at 
  FROM meal m 
  WHERE m.id = p_meal_id;
END;
$$;
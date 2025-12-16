-- food rls policies --

CREATE POLICY "select_food" 
ON public.food 
FOR SELECT 
TO authenticated 
USING (true);

CREATE POLICY "insert_food" 
ON public.food 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "update_food" 
ON public.food 
FOR UPDATE 
TO authenticated 
USING (true) 
WITH CHECK (true);

CREATE POLICY "delete_food" 
ON public.food 
FOR DELETE 
TO authenticated 
USING (true);

-- document rls policies --

CREATE POLICY "select_document" 
ON public.document 
FOR SELECT 
TO authenticated 
USING (true);

CREATE POLICY "insert_document" 
ON public.document 
FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "update_document" 
ON public.document 
FOR UPDATE 
TO authenticated 
USING (true) 
WITH CHECK (true);

CREATE POLICY "delete_document" 
ON public.document 
FOR DELETE 
TO authenticated 
USING (true);

-- meal rls policies --

CREATE POLICY "select_own_meal" 
ON public.meal 
FOR SELECT 
TO authenticated 
USING (user_id = auth.uid());

CREATE POLICY "insert_own_meal" 
ON public.meal 
FOR INSERT 
TO authenticated 
WITH CHECK (user_id = auth.uid());

CREATE POLICY "update_own_meal" 
ON public.meal 
FOR UPDATE 
TO authenticated 
USING (user_id = auth.uid()) 
WITH CHECK (user_id = auth.uid());

CREATE POLICY "delete_own_meal" 
ON public.meal 
FOR DELETE 
TO authenticated 
USING (user_id = auth.uid());

-- meal_food rls policies --

CREATE POLICY "select_own_meal_food" 
ON public.meal_food 
FOR SELECT 
TO authenticated 
USING (
  EXISTS (
    SELECT 1 
    FROM meal 
    WHERE meal.id = meal_food.meal_id 
      AND meal.user_id = auth.uid()
  )
);

CREATE POLICY "insert_own_meal_food" 
ON public.meal_food 
FOR INSERT 
TO authenticated 
WITH CHECK (
  EXISTS (
    SELECT 1 
    FROM meal 
    WHERE meal.id = meal_food.meal_id 
      AND meal.user_id = auth.uid()
  )
);

CREATE POLICY "update_own_meal_food" 
ON public.meal_food 
FOR UPDATE 
TO authenticated 
USING (
  EXISTS (
    SELECT 1 
    FROM meal 
    WHERE meal.id = meal_food.meal_id 
      AND meal.user_id = auth.uid()
  )
) 
WITH CHECK (
  EXISTS (
    SELECT 1 
    FROM meal 
    WHERE meal.id = meal_food.meal_id 
      AND meal.user_id = auth.uid()
  )
);

CREATE POLICY "delete_own_meal_food" 
ON public.meal_food 
FOR DELETE 
TO authenticated 
USING (
  EXISTS (
    SELECT 1 
    FROM meal 
    WHERE meal.id = meal_food.meal_id 
      AND meal.user_id = auth.uid()
  )
);

-- symptom rls policies --

CREATE POLICY "select_own_symptoms" 
ON public.symptom 
FOR SELECT 
TO authenticated 
USING (user_id = auth.uid());

CREATE POLICY "insert_own_symptoms" 
ON public.symptom 
FOR INSERT 
TO authenticated 
WITH CHECK (user_id = auth.uid());

CREATE POLICY "update_own_symptoms" 
ON public.symptom 
FOR UPDATE 
TO authenticated 
USING (user_id = auth.uid()) 
WITH CHECK (user_id = auth.uid());

CREATE POLICY "delete_own_symptoms" 
ON public.symptom 
FOR DELETE 
TO authenticated 
USING (user_id = auth.uid());
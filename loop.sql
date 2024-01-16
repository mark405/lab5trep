DO $$
DECLARE
    store INT;
    store_type VARCHAR(255);
    store_size INT;
    counter INT := 5;
BEGIN
    -- Start the loop
    WHILE counter <= 10 LOOP
        -- Generate test data
        store := counter;
        store_type := 'Type ' || counter;
        store_size := counter * 100;

        -- Insert data into the Stores table
        INSERT INTO Stores(store, type, size)
        VALUES (store, store_type, store_size);

        -- Increment the counter
        counter := counter + 1;
    END LOOP;
END $$;
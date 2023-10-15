CREATE OR REPLACE FUNCTION insert_deliveryman_balance()
RETURNS trigger AS
$$
BEGIN
    INSERT INTO "balances" ( "deliveryman_id", "sum")
         VALUES(NEW."id", 0);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER deliveryman_save_trigger
AFTER INSERT
ON "deliverymen"
FOR EACH ROW
EXECUTE PROCEDURE insert_deliveryman_balance();

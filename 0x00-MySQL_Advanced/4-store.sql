-- Create trigger if it does not exist

CREATE TRIGGER `decrease_order` AFTER INSERT
ON `orders` FOR EACH ROW UPDATE items
SET quantity = quantity - NEW.number
WHERE name = New.item_name;

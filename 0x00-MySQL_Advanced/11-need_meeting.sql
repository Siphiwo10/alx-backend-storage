-- Create view if it does not exist

DELIMITER $$

DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT  name
FROM students
WHERE score < 80
AND last_meeting IS NULL OR DATE(NOW()) > DATE_ADD(last_meeting, INTERVAL 1 MONTH);
DELIMITER ;

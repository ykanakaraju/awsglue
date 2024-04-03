UPDATE cdcdb.Persons SET FullName = 'John Doe' WHERE PersonId = 1;
INSERT INTO cdcdb.Persons VALUES (100,'Linda Johnson','New York');
INSERT INTO cdcdb.Persons VALUES (101,'William Johnson','Phoenix');
INSERT INTO cdcdb.Persons VALUES (102,'Will Smith','Tempe');
UPDATE cdcdb.Persons SET FullName = 'John Doe' WHERE PersonId = 3;
DELETE FROM cdcdb.Persons WHERE PersonId = 10;
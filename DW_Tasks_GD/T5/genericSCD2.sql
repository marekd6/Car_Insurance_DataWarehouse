CREATE VIEW SCDview
AS
SELECT
	BK,
	category1,
	category2
FROM DB.TB
;
GO

DECLARE @Yesterday DATE;
SET @Yesterday = DATEADD(year, -1, GETDATE());
--SET @Yesterday = DATEADD(day, -1, GETDATE());
DECLARE @Today DATE;
SET @Today = DATEADD(year, -100, GETDATE());
--SET @Today = GETDATE();


MERGE INTO DT as TT
	USING SCDview as ST
		ON TT.BK = ST.BK
			WHEN Not Matched -- simple INSERT when no value
				THEN
					INSERT Values (
					ST.BK,
					ST.category1,
					ST.category1,
					@Today, --insertion date
					NULL, --deactivation date
					1 --Is_Current flag
					)
			WHEN Matched -- BK matched
				AND TT.Is_Current = 1 -- change only the previous version
				-- but not the rest
				AND (ST.category1 <> TT.category1
					OR ST.category2 <> TT.category2)
			THEN
				UPDATE -- mark old tuple as obsolete
					SET TT.Is_Current = 0,
					TT.Deactivation_date = @Today
			WHEN Not Matched BY Source
			AND TT.BK != 'unknownvalue' -- do not update the UNKNOWN tuple
			THEN
				UPDATE
				SET TT.Is_Current = 0,
					TT.Deactivation_date = @Today
;


-- inserting changed rows to the DT table
INSERT INTO DT(
	BK, 
	category1,
	category2, 
	Insertion_date, 
	Deactivation_date, 
	Is_Current
	)
	SELECT 
		BK, 
		category1, 
		category2, 
		@Yesterday, 
		NULL, 
		1
	FROM SCDview
	EXCEPT
	SELECT 
		BK, 
		category1, 
		category2, 
		@Yesterday, 
		NULL, 
		1 
	FROM DT
;
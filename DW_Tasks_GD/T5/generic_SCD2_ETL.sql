--supplementary material resulting from participation in DW course 2023
--by Marek Drwal, 16.06.23

--a generic T-SQL code for loading Slowly Changing Dimension type 2 into Data Warehouse in ETL process;
--a star schema is considered;

--first, a view is created;
--it contains the Business Key and other attributes of SCD
--extracted and transformed from sources (DB, CSV, etc.)
IF (object_id('SCDview') IS NOT NULL) DROP VIEW SCDview;
GO
CREATE VIEW SCDview AS
	SELECT
		BK,
		attribute1, --some attributes match DW design
		attribute2, --and can be used directly
		CASE --while some require more or less preparation
			WHEN category3 = 'M' THEN 'male'
			ELSE 'female'
		END AS attribute3,
	FROM DB.Tscd --sources
;
GO

--two ancillary variables are declared to handle date issue;
--in reality, one date would be enough, namely Today;
--current date would be used to set insertion and deactivation dates
--every time the ETL is run;
--yet, for demonstration, it should be differentiated;
--Yesterday is the day of deactivating a tuple
--and Today - the day of update or insert;
DECLARE @Today DATE;
SET @Today = GETDATE();
DECLARE @Yesterday DATE;
SET @Yesterday = DATEADD(day, -1, GETDATE());

--structure of a SCD2 DT
--(PK-ID, BK, attribute1, attribute2, attribute3, Insertion_date, Deactivation_date, Is_Current);

--then, a MERGE statement is issued;
--it either inserts new tuples from the source view into the DT (when BK is not found in the DT)
--or marks the existing tuple in the DT as obsolete
--(when BK is matched but other slowy changing details are not
--or when the tuple is no longer present in the source view);
--an issue of design is to determine which SCD attributes may change
--causing UPDATE and INSERT
--and which not, having no impact on DW;
MERGE INTO DW.DT as TT --(Slowly Changing) Dimension Table as a target
	USING SCDview as ST --the view as a source
		ON TT.BK = ST.BK --Business Keys as linkers
			WHEN NOT MATCHED --the dimension member from view (ST) not found in the DT (TT)
			THEN
				INSERT Values ( --new member is inserted
					ST.BK, --Dimension Business Key
					ST.attribute1, --attributes
					ST.attribute2, 
					ST.attribute3,
					@Today, --insertion date
					NULL, --deactivation date
					1 --Is_Current flag
					)
			WHEN MATCHED --BK matched (same in the view (ST) and DT (TT))
				AND TT.Is_Current = 1 --change only the previous version
						--but other attributes do not match (they differ between ST and TT)
				AND (ST.attribute1 <> TT.attribute1
					OR ST.attribute2 <> TT.attribute2
					OR ST.attribute3 <> TT.attribute3)
			THEN
				UPDATE --mark old tuple (in DT (TT)) as obsolete
					SET TT.Is_Current = 0,
					TT.Deactivation_date = @Yesterday
			WHEN NOT MATCHED BY Source --tuple not found in ST while present in TT
				AND TT.BK != 'unknownvalue' -- do not update the UNKNOWN tuple
			THEN
				UPDATE --mark as obsolete
				SET TT.Is_Current = 0,
					TT.Deactivation_date = @Yesterday
;
GO

--finally, new tuples have to be inserted into DT separately;
--all tuples from the view that are not present in the DT are selected;
INSERT INTO DW.DT (BK, attribute1, attribute2, attribute3, Insertion_date, Deactivation_date, Is_Current)
	SELECT 
		BK, 
		attribute1, 
		attribute2, 
		attribute3,
		@Today, 
		NULL, 
		1
	FROM SCDview
	EXCEPT
	SELECT 
		BK, 
		attribute1, 
		attribute2, 
		attribute3,
		@Today, 
		NULL, 
		1 
	FROM DW.DT
;
GO

DROP VIEW SCDview;
GO
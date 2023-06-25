USE Car_Insurance
GO

-- Client
-- Preprocessing the data (Sex, Age, and Driving_experience)
CREATE VIEW vETLDimClientsData
AS
SELECT DISTINCT
	ID,
	PESEL,
	CASE
		WHEN Sex = 'M' THEN 'male'
		ELSE 'female'
	END AS Sex,
	CASE
		WHEN Date_of_birth > '2001-01-01' THEN 'from 18 to 21'
		WHEN Date_of_birth > '1993-01-01' THEN 'from 22 to 29'
		WHEN Date_of_birth > '1973-01-01' THEN 'from 30 to 49'
		WHEN Date_of_birth > '1959-01-01' THEN 'from 50 to 64'
		ELSE 'more than 64'
	END AS Age,
	CASE
		WHEN License_issuing_date > '2022-01-01' THEN 'up to one year'
		WHEN License_issuing_date > '2018-01-01' THEN 'between one and five years'
		WHEN License_issuing_date > '2013-01-01' THEN 'between five and ten years'
		ELSE 'more than ten years'
	END AS Driving_experience,
	Voivodeship
FROM SureSale.dbo.Clients;
GO

CREATE TABLE #Temp
(
	ID_Client int IDENTITY(1,1),
	PESEL char(11) NOT NULL,
	Sex varchar(6) NOT NULL,
	Age varchar(13) NOT NULL,
	Driving_experience varchar(26) NOT NULL,
	Voivodeship varchar(25) NOT NULL,
	Insertion_date date NOT NULL,
	Deactivation_date date,
	Is_Current bit NOT NULL,

	CONSTRAINT proper_PESEL
		CHECK(PESEL LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
);
GO

-- Declare variables use in processing
DECLARE @Yesterday DATE;
SET @Yesterday = DATEADD(day, -1, GETDATE());
DECLARE @Today DATE;
SET @Today = GETDATE();

-- Outer insert - the updated records are added to the SCD2 table
-- You gotta love Microsoft: https://stackoverflow.com/questions/2642504/scd2-merge-statement-sql-server
INSERT INTO #Temp (PESEL, Sex, Age, Driving_experience, Voivodeship, Insertion_date, Is_Current)
SELECT PESEL, Sex, Age, Driving_experience, Voivodeship, @Today, 1
FROM
(
-- Merge statement
MERGE INTO dbo.DT_Client AS DST
USING vETLDimClientsData AS SRC
ON (SRC.ID = DST.ID_Client)
-- New records inserted
WHEN NOT MATCHED THEN 
INSERT (PESEL, Sex, Age, Driving_experience, Voivodeship, Insertion_date, Is_Current)
VALUES (SRC.PESEL, SRC.Sex, SRC.Age, SRC.Driving_experience, SRC.Voivodeship, @Today, 1)
-- Existing records updated if data changes
WHEN MATCHED 
AND Is_Current = 1
AND (
 ISNULL(DST.PESEL,'') <> ISNULL(SRC.PESEL,'') 
 OR ISNULL(DST.Sex,'') <> ISNULL(SRC.Sex,'') 
 OR ISNULL(DST.Age,'') <> ISNULL(SRC.Age,'')
 OR ISNULL(DST.Driving_experience,'') <> ISNULL(SRC.Driving_experience,'')
 OR ISNULL(DST.Voivodeship,'') <> ISNULL(SRC.Voivodeship,'')
 )
-- Update statement for a changed dimension record, to flag as no longer active
THEN UPDATE 
SET DST.Is_Current = 0, DST.Deactivation_date = @Yesterday
OUTPUT SRC.PESEL, SRC.Sex, SRC.Age, SRC.Driving_experience, SRC.Voivodeship, $Action AS MergeAction
) AS MRG
WHERE MRG.MergeAction = 'UPDATE'
;

INSERT INTO dbo.DT_Client (PESEL, Sex, Age, Driving_experience, Voivodeship, Insertion_date, Deactivation_date, Is_Current)
SELECT PESEL, Sex, Age, Driving_experience, Voivodeship, Insertion_date, Deactivation_date, Is_Current FROM #Temp;

DROP TABLE #Temp;
DROP VIEW vETLDimClientsData;
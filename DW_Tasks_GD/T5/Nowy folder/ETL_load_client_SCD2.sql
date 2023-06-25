use Car_Insurance
go-- SCD 2

-- Preprocessing the data (Sex, Age, and Driving_experience)
If (object_id('vETLDimClientsData') is not null) Drop View vETLDimClientsData;
go
CREATE VIEW vETLDimClientsData
AS
SELECT
	PESEL,
	CASE
		WHEN Sex = 'M' THEN 'male'
		ELSE 'female'
	END AS Sex,
	CASE
		WHEN DATEDIFF(year, [Date_of_birth], CURRENT_TIMESTAMP) BETWEEN 18 AND 21 THEN 'from 18 to 21'
		WHEN DATEDIFF(year, [Date_of_birth], CURRENT_TIMESTAMP) BETWEEN 22 AND 29 THEN 'from 22 to 29'
		WHEN DATEDIFF(year, [Date_of_birth], CURRENT_TIMESTAMP) BETWEEN 30 AND 49 THEN 'from 30 to 49'
		WHEN DATEDIFF(year, [Date_of_birth], CURRENT_TIMESTAMP) BETWEEN 50 AND 64 THEN 'from 50 to 64'
		ELSE 'more than 64'
	END AS Age,
	CASE
		WHEN DATEDIFF(year, [License_issuing_date], CURRENT_TIMESTAMP) <=1 THEN 'up to one year'
		WHEN DATEDIFF(year, [License_issuing_date], CURRENT_TIMESTAMP) BETWEEN 1 AND 5 THEN 'between one and five years'
		WHEN DATEDIFF(year, [License_issuing_date], CURRENT_TIMESTAMP) BETWEEN 5 AND 10 THEN 'between five and ten years'
		ELSE 'more than ten years'
	END AS Driving_experience,
	Voivodeship
FROM SureSale.dbo.Clients;
GO

DECLARE @Yesterday DATE;
--SET @Yesterday = DATEADD(year, -1, GETDATE()); why?
SET @Yesterday = DATEADD(day, -1, GETDATE());
DECLARE @Today DATE;
--SET @Today = DATEADD(year, -100, GETDATE()); why?
SET @Today = GETDATE();

MERGE INTO DT_Client as TT
	USING vETLDimClientsData as ST
		ON TT.PESEL = ST.PESEL
			WHEN Not Matched -- simple INSERT
				THEN
					INSERT Values (
					ST.PESEL,
					ST.Sex,
					ST.Age,
					ST.Driving_experience,
					ST.Voivodeship,
					@Today,
					NULL,
					1
					)
			WHEN Matched -- PESEL matched
			AND TT.Is_Current = 1 -- change only the previous version
			-- but not Age
				AND (ST.Age <> TT.Age
			-- or the Driving_experience level...
				OR ST.Driving_experience <> TT.Driving_experience
			-- or Voivodeship
				OR ST.Voivodeship <> TT.Voivodeship)
			THEN
				UPDATE -- mark old tuple as obsolete
				SET TT.Is_Current = 0,
				TT.Deactivation_date = @Today
			WHEN Not Matched BY Source
			AND TT.PESEL != '12345678901' -- do not update the UNKNOWN tuple
			THEN
				UPDATE
				SET TT.Is_Current = 0,
					TT.Deactivation_date = @Today
			;

-- INSERTING CHANGED ROWS TO THE DT_Client TABLE
INSERT INTO DT_Client(
	PESEL, 
	Sex,
	Age, 
	Driving_experience, 
	Voivodeship,
	Insertion_date, 
	Deactivation_date, 
	Is_Current
	)
	SELECT 
		PESEL, 
		Sex, 
		Age, 
		Driving_experience, 
		Voivodeship,
		@Yesterday, 
		NULL, 
		1
	FROM vETLDimClientsData
	EXCEPT
	SELECT 
		PESEL, 
		Sex, 
		Age, 
		Driving_experience, 
		Voivodeship,
		@Yesterday, 
		NULL, 
		1 
	FROM DT_Client;

Drop View vETLDimClientsData;
GO
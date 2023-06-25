USE Car_Insurance
GO

-- load CSV file
IF (object_id('dbo.PartsCatalogueTemp') is not null) DROP TABLE [dbo].[PartsCatalogueTemp];
GO

CREATE TABLE [dbo].[PartsCatalogueTemp](Part VARCHAR(25), FK_CarType INT, PartValue SMALLMONEY);
GO

BULK INSERT [dbo].[PartsCatalogueTemp] FROM 'C:\Users\piotr\OneDrive\Pulpit\DW\CSVs\parts.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);
GO

-- transpose the CSV file (i.e., create individual columns for different parts)
IF (object_id('dbo.PartsCatalogueTransposed') is not null) DROP VIEW [dbo].[PartsCatalogueTransposed];
GO

CREATE VIEW PartsCatalogueTransposed
AS
SELECT *
FROM (
		SELECT [FK_CarType], [Part], [PartValue]
		FROM [dbo].[PartsCatalogueTemp]
	 )
	 AS ST PIVOT(AVG([PartValue]) FOR [Part] IN ([Engine],
											   [Front_doors],
											   [Rear_doors],
											   [Left_mirror],
											   [Right_mirror],
											   [Front_headlights],
											   [Rear_headlights],
											   [Front_bumper], 
											   [Rear_bumper])) AS PT;
GO

IF (object_id('dbo.vETLFactClaimsAuxilary') is not null) DROP VIEW [dbo].[vETLFactClaimsAuxilary];
GO

CREATE VIEW vETLFactClaimsAuxilary
AS
SELECT Claims.ID AS ID_Claim,
	   Claims.Submission_date AS Submission_Date,
	   Claims.Evaluation_date AS Assessment_date,
	   Clients.ID AS ID_Client,
	   Cars.ID AS ID_Car,
	   Assessors.ID AS ID_Assessor,
	   PCatalogue.Engine AS Engine_value,
	   PCatalogue.Front_doors AS Front_doors_value,
	   PCatalogue.Rear_doors AS Rear_doors_value,
	   PCatalogue.Left_mirror AS Left_mirror_value,
	   PCatalogue.Right_mirror AS Right_mirror_value,
	   PCatalogue.Front_headlights AS Front_headlights_value,
	   PCatalogue.Rear_headlights AS Rear_headlights_value,
	   PCatalogue.Front_bumper AS Front_bumper_value,
	   PCatalogue.Rear_bumper AS Rear_bumper_value,
	   Claims.Engine AS Engine_damage,
	   Claims.Front_doors AS Front_doors_damage,
	   Claims.Rear_doors AS Rear_doors_damage,
	   Claims.Left_mirror AS Left_mirror_damage,
	   Claims.Right_mirror AS Right_mirror_damage,
	   Claims.Front_headlights AS Front_headlights_damage,
	   Claims.Rear_headlights AS Rear_headlights_damage,
	   Claims.Front_bumper AS Front_bumper_damage,
	   Claims.Rear_bumper AS Rear_bumper_damage,
	   CASE -- this part should work as a simple IF, but for an unclear reason SQL Server refuses to cooperate
			WHEN Claims.Engine = 0 THEN 0
			ELSE 1
	   END AS Engine_damage_binary,
	   CASE
			WHEN Claims.Front_doors = 0 THEN 0
			ELSE 1
		END AS Front_doors_damage_binary,
		CASE
			WHEN Claims.Rear_doors = 0 THEN 0
			ELSE 1
		END AS Rear_doors_damage_binary,
		CASE
			WHEN Claims.Left_mirror = 0 THEN 0
			ELSE 1
		END AS Left_mirror_damage_binary,
		CASE
			WHEN Claims.Right_mirror = 0 THEN 0
			ELSE 1
		END AS Right_mirror_damage_binary,
		CASE
			WHEN Claims.Front_headlights = 0 THEN 0
			ELSE 1
		END AS Front_headlights_damage_binary,
		CASE
			WHEN Claims.Rear_headlights = 0 THEN 0
			ELSE 1
		END AS Rear_headlights_damage_binary,
		CASE
			WHEN Claims.Front_bumper = 0 THEN 0
			ELSE 1
		END AS Front_bumper_damage_binary,
		CASE
			WHEN Claims.Rear_bumper = 0 THEN 0
			ELSE 1
		END AS Rear_bumper_damage_binary
FROM
	[dbo].[PartsCatalogueTransposed] AS PCatalogue
	JOIN [SureSale].[dbo].[Car_Types] AS CTypes
		ON PCatalogue.FK_CarType = CTypes.ID
	JOIN [SureSale].[dbo].[Cars] AS Cars
		ON CTypes.ID = Cars.Car_type_ID
	JOIN [SureSale].[dbo].[Insurances] AS Insurances
		ON Cars.ID = Insurances.Car_ID
	JOIN [SureSale].[dbo].[Clients] AS Clients
		ON Insurances.Client_ID = Clients.ID
	JOIN [SureSale].[dbo].[Claims] AS Claims
		ON Insurances.ID = Claims.Insurance_ID
	JOIN [SureSale].[dbo].[Assessors] AS Assessors
		ON Claims.Assessor_ID = Assessors.ID;
GO

IF (object_id('dbo.vETLFactClaimData1') is not null) DROP VIEW [dbo].[vETLFactClaimData1];
GO

CREATE VIEW vETLFactClaimData1
AS
SELECT ID_Claim,
	   Assessment_date,
	   Submission_date,
	   ID_Client,
	   ID_Car,
	   ID_Assessor,
	   Engine_damage_binary + Front_doors_damage_binary +
	   Rear_doors_damage_binary + Left_mirror_damage_binary +
	   Right_mirror_damage_binary + Front_headlights_damage_binary +
	   Rear_headlights_damage_binary + Front_bumper_damage_binary +
	   Rear_bumper_damage_binary
		AS Number_of_damaged_parts,
	   Engine_value * Engine_damage * 0.5 AS Engine_cost,
	   Front_doors_value * Front_doors_damage * 0.5 AS Front_doors_cost,
	   Rear_doors_value * Rear_doors_damage * 0.5 AS Rear_doors_cost,
	   Left_mirror_value * Left_mirror_damage * 0.5 AS Left_mirror_cost,
	   Right_mirror_value * Right_mirror_damage * 0.5 AS Right_mirror_cost,
	   Front_headlights_value * Front_headlights_damage * 0.5 AS Front_headlights_cost,
	   Rear_headlights_value * Rear_headlights_damage * 0.5 AS Rear_headlights_cost,
	   Front_bumper_value * Front_bumper_damage * 0.5 AS Front_bumper_cost,
	   Rear_bumper_value * Rear_bumper_damage * 0.5 AS Rear_bumper_cost
FROM
	[dbo].[vETLFactClaimsAuxilary];
GO

IF (object_id('dbo.vETLFactClaimData2') is not null) DROP VIEW [dbo].[vETLFactClaimData2];
GO

CREATE VIEW vETLFactClaimData2
AS
SELECT ID_Claim,
	   Assessment_date,
	   Submission_date,
	   ID_Client,
	   ID_Car,
	   ID_Assessor,
	   Number_of_damaged_parts,
	   Engine_cost,
	   Front_doors_cost,
	   Rear_doors_cost,
	   Left_mirror_cost,
	   Right_mirror_cost,
	   Front_headlights_cost,
	   Rear_headlights_cost,
	   Front_bumper_cost,
	   Rear_bumper_cost,
	   Engine_cost + Front_doors_cost + Rear_doors_cost +
	   Left_mirror_cost + Right_mirror_cost + Front_headlights_cost +
	   Rear_headlights_cost + Front_bumper_cost + Rear_bumper_cost
		AS Indemnity
FROM
	[dbo].[vETLFactClaimData1];
GO



IF (object_id('dbo.vETLFClaim') is not null) DROP VIEW [dbo].[vETLFClaim];
GO

CREATE VIEW vETLFClaim
AS
SELECT  Number_of_damaged_parts,
	    Engine_cost,
	    Front_doors_cost,
	    Rear_doors_cost,
	    Left_mirror_cost,
	    Right_mirror_cost,
	    Front_headlights_cost,
	    Rear_headlights_cost,
	    Front_bumper_cost,
	    Rear_bumper_cost,
	    Indemnity,
		ID_Assessment_Date = ADate.ID_Date,
		ID_Submission_Date = SDate.ID_Date,
		ID_Car = Claim.ID_Car,
		ID_Assessor = Claim.ID_Assessor,
		ID_Client = Claim.ID_Client
FROM 
	[dbo].[vETLFactClaimData2] AS Claim
	JOIN [dbo].[DT_Date] AS ADate
		ON CONVERT(VARCHAR(10), ADate.Date, 111) = CONVERT(VARCHAR(10), Claim.Assessment_date, 111)
	JOIN [dbo].[DT_Date] AS SDate
		ON CONVERT(VARCHAR(10), SDate.Date, 111) = CONVERT(VARCHAR(10), Claim.Submission_date, 111)
	JOIN [dbo].[DT_Car] AS Car
		ON Car.ID_Car = Claim.ID_Car
	JOIN [dbo].[DT_Assessor] AS Assessor
		ON Assessor.ID_Assessor = Claim.ID_Assessor
	JOIN [dbo].[DT_Client] AS Client
		ON Claim.ID_Client = Client.ID_Client AND Client.Is_Current = 1
	;
GO

MERGE INTO [dbo].[FT_Claim] AS TT
	USING [dbo].[vETLFClaim] AS ST
		ON TT.ID_Assessment_Date = ST.ID_Assessment_Date AND
		   TT.ID_Submission_Date = ST.ID_Submission_Date AND
		   TT.ID_Car = ST.ID_Car AND
		   TT.ID_Assessor = ST.ID_Assessor AND
		   TT.ID_Client = ST.ID_Client
				WHEN Not Matched
					THEN
						INSERT VALUES (
										  ST.ID_Assessment_Date,
										  ST.ID_Submission_Date,
										  ST.ID_Client,
										  ST.ID_Car,
										  ST.ID_Assessor,
										  ST.Number_of_damaged_parts,
										  ST.Engine_cost,
										  ST.Front_doors_cost,
										  ST.Rear_doors_cost,
										  ST.Left_mirror_cost,
										  ST.Right_mirror_cost,
										  ST.Front_headlights_cost,
										  ST.Rear_headlights_cost,
										  ST.Front_bumper_cost,
										  ST.Rear_bumper_cost,
										  ST.Indemnity
									  )
;
	
DROP VIEW [dbo].[vETLFClaim];
DROP VIEW [dbo].[vETLFactClaimData2];
DROP VIEW [dbo].[vETLFactClaimData1];
DROP VIEW [dbo].[vETLFactClaimsAuxilary];
DROP VIEW [dbo].[PartsCatalogueTransposed];
DROP TABLE [dbo].[PartsCatalogueTemp];
USE Car_Insurance
GO
-- Car - done
If (object_id('vETLDimCarsData') is not null) Drop View vETLDimCarsData;
go

CREATE VIEW vETLDimCarsData
AS
SELECT --DISTINCT
	Cars.ID AS CarID,
	Cars.VIN,
	Types.Class,
	Types.Size,
	Cars.Colour
FROM SureSale.dbo.Cars AS Cars
JOIN SureSale.dbo.Car_Types AS Types
ON Cars.Car_type_ID = Types.ID;
go

MERGE INTO DT_Car as TT
	USING vETLDimCarsData as ST
		ON TT.VIN = ST.VIN
			WHEN Not Matched
				THEN
					INSERT
					Values (
					ST.VIN, ST.Class, ST.[Size], ST.Colour
					)
			--WHEN Not Matched By Source
				--Then
					--DELETE
			;

Drop View vETLDimCarsData;
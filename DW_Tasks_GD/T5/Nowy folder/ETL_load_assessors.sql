USE Car_Insurance
GO

If (object_id('vETLDimAssessorsData') is not null) Drop View vETLDimAssessorsData;
go

CREATE VIEW vETLDimAssessorsData
AS
SELECT DISTINCT
	[ID] as [AssessorID],
	[Name_and_Surname] = Cast([Name] + ' ' + [Surname] as nvarchar(50)),
	Specialisation
FROM SureSale.dbo.Assessors;
go

MERGE INTO DT_Assessor as TT
	USING vETLDimAssessorsData as ST
		ON TT.Name_and_Surname = ST.Name_and_Surname
			WHEN Not Matched
				THEN
					INSERT
					Values (
					ST.Name_and_Surname, ST.Specialisation
					)
			--WHEN Not Matched By Source
				--Then
					--DELETE
			;

Drop View vETLDimAssessorsData;
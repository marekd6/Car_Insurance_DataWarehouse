use Car_Insurance
go

SET IDENTITY_INSERT dbo.DT_Date ON;  
GO

INSERT INTO dbo.DT_Date(ID_Date, "Date", "Year", "Month", "MonthNo", "Day") 
Values(-1, '1970-01-01', '1970', 'January', 1, 1);
go

SET IDENTITY_INSERT dbo.DT_Date OFF;  
GO

SET IDENTITY_INSERT dbo.DT_Assessor ON;  
GO

INSERT INTO dbo.DT_Assessor(ID_Assessor, Name_and_Surname, Specialisation) 
Values(-1, 'Unknown', 'cargo');
go

SET IDENTITY_INSERT dbo.DT_Assessor OFF;  
GO

SET IDENTITY_INSERT dbo.DT_Car ON;  
GO

INSERT INTO dbo.DT_Car(ID_Car, VIN, "Class", "Size", Colour) 
Values(-1, '12345678901234567', 'premium', 'small', 'black');
go

SET IDENTITY_INSERT dbo.DT_Car OFF;  
GO

SET IDENTITY_INSERT dbo.DT_Client ON;  
GO

INSERT INTO dbo.DT_Client(ID_Client, PESEL, Sex, "Age", Driving_experience, Voivodeship, Insertion_date, Deactivation_date, Is_Current) 
Values(-1, '12345678901', 'male', 'from 18 to 21', 'up to one year', 'Pomorskie', '1970-01-01', NULL, 1);
go

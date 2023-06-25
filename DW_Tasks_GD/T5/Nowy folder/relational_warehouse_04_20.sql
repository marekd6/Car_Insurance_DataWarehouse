CREATE DATABASE [Car_Insurance]
GO

USE [Car_Insurance]
GO

CREATE TABLE [dbo].[DT_Date](
	[ID_Date] [int] IDENTITY(1,1) PRIMARY KEY,
	[Date] [date] NOT NULL,
	[Year] [varchar](4) NOT NULL,
	[Month] [varchar](10) NOT NULL,
	[MonthNo] [tinyint] NOT NULL,
	[Day] [varchar](10) NOT NULL
)
GO

CREATE TABLE DT_Assessor(
	ID_Assessor int IDENTITY(1,1) PRIMARY KEY,
	Name_and_Surname varchar(50) NOT NULL,
	Specialisation varchar(7) NOT NULL
)
GO

CREATE TABLE DT_Car(
	ID_Car int IDENTITY(1,1) PRIMARY KEY,
	VIN char(17) NOT NULL,
	Class varchar(7) NOT NULL,
	Size varchar(6) NOT NULL,
	Colour varchar(15) NOT NULL
)
GO

CREATE TABLE DT_Client(
	ID_Client int IDENTITY(1,1) PRIMARY KEY,
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
)
GO

CREATE TABLE [dbo].[FT_Claim](
	ID_Assessment_Date int REFERENCES DT_Date,
	ID_Submission_Date int REFERENCES DT_Date,
	ID_Client int REFERENCES DT_Client,
	ID_Car int REFERENCES DT_Car,
	ID_Assessor int REFERENCES DT_Assessor,
	Number_of_damaged_parts tinyint,
	Indemnity money,
	Engine_cost smallmoney,
	Front_doors_cost smallmoney,
	Rear_doors_cost smallmoney,
	Left_mirror_cost smallmoney,
	Right_mirror_cost smallmoney,
	Front_headlights_cost smallmoney,
	Rear_headlights_cost smallmoney,
	Front_bumper_cost smallmoney,
	Rear_bumper_cost smallmoney,
	PRIMARY KEY(ID_Assessment_Date, ID_Submission_Date, ID_Client, ID_Car, ID_Assessor, Number_of_damaged_parts)
)
GO
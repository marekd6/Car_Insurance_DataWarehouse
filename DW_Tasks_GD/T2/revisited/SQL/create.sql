CREATE DATABASE SureSale
GO

USE SureSale
GO

CREATE TABLE Clients
( 
	ID INTEGER PRIMARY KEY,
	PESEL Char(11) NOT NULL UNIQUE,--missing
	Name1 VarChar(25) NOT NULL, 
	Name2 VarChar(25), 
	Surname VarChar(25) NOT NULL, 
	Sex Char(1) CHECK(Sex IN('F', 'M')), 
	Date_of_birth DATE NOT NULL, 
	Voivodeship VarChar(25) NOT NULL, 
	City VarChar(30) NOT NULL, 
	Street_and_number VarChar(55) NOT NULL, 
	Account_nb Char(28) NOT NULL, 
	License_issuing_date DATE NOT NULL,
	
	CONSTRAINT proper_PESEL
		CHECK(PESEL LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
) 
GO  

CREATE TABLE Car_Types
(
	ID INTEGER PRIMARY KEY,
	Class VarChar(7) NOT NULL,
	Size VarChar(6) NOT NULL,--typo
	Production_year INTEGER NOT NULL
)
GO

CREATE TABLE Cars 
( 	
	ID INTEGER PRIMARY KEY, 
	VIN Char(17), 
	Registration_ID Char(7) NOT NULL, 
	Car_type_ID INTEGER NOT NULL REFERENCES Car_Types,
	Colour VarChar(15) NOT NULL, 
	Engine_capacity FLOAT NOT NULL
)
GO	

CREATE TABLE Ownership
(
	Client_ID INTEGER REFERENCES Clients,
	Car_ID INTEGER REFERENCES Cars,
	PRIMARY KEY(Client_ID, Car_ID)
)
GO

CREATE TABLE Agents
(
	ID INTEGER PRIMARY KEY, 
	Name VarChar(25) NOT NULL,
	Surname VarChar(25) NOT NULL,
	Voivodeship VarChar(25) NOT NUll
)
GO

CREATE TABLE Insurances 
( 
	ID INTEGER PRIMARY KEY, 
	Sale_date DATE NOT NULL, 
	Mileage INTEGER NOT NULL CHECK(Mileage>0), 
	Garage BIT NOT NULL, /*Boolean*/ 
	Price SMALLMONEY NOT NULL,
	Client_ID INTEGER NOT NULL REFERENCES Clients,
	Car_ID INTEGER REFERENCES Cars,
	Agent_ID INTEGER NOT NULL REFERENCES Agents
)
GO	

CREATE TABLE Assessors
(
	ID INTEGER PRIMARY KEY, 
	Name VarChar(25) NOT NULL,
	Surname VarChar(25) NOT NULL,
	Specialisation VarChar(7) NOT NUll CHECK(Specialisation IN('cargo', 'premium', 'casual'))
)
GO

CREATE TABLE Claims 
( 
	ID INTEGER PRIMARY KEY, 
	Submission_date DATE NOT NULL, 
	Parking_place VarChar(90) NOT NULL, 
	Assessor_ID INTEGER NOT NULL REFERENCES Assessors, 
	Evaluation_date DATE NOT NULL,
	Engine tinyint NOT NULL,
	Front_doors tinyint NOT NULL,
	Rear_doors tinyint NOT NULL,
	Left_mirror tinyint NOT NULL,
	Right_mirror tinyint NOT NULL,
	Front_headlights tinyint NOT NULL,
	Rear_headlights tinyint NOT NULL,
	Front_bumper tinyint NOT NULL,
	Rear_bumper tinyint NOT NULL,
	Insurance_ID INTEGER NOT NULL REFERENCES Insurances
)
GO

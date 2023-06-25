use SureSale
GO

BULK INSERT dbo.Car_Types FROM 'C:\Users\laptop\Desktop\DW_generator\car_types.csv' 
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');

BULK INSERT dbo.Cars FROM 'C:\Users\laptop\Desktop\DW_generator\cars.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');

BULK INSERT dbo.Parts FROM 'C:\Users\laptop\Desktop\DW_generator\parts.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');

BULK INSERT dbo.Clients FROM 'C:\Users\laptop\Desktop\DW_generator\clients.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');

BULK INSERT dbo.Insurances FROM 'C:\Users\laptop\Desktop\DW_generator\insurances.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');

BULK INSERT dbo.Claims FROM 'C:\Users\laptop\Desktop\DW_generator\claims2.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      , ROWTERMINATOR = '0x0a');
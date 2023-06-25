use SureSale
GO

BULK INSERT dbo.Car_Types FROM 'C:\Users\laptop\Desktop\DW_generator\car_types.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Cars FROM 'C:\Users\laptop\Desktop\DW_generator\cars.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Agents FROM 'C:\Users\laptop\Desktop\DW_generator\agents.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Assessors FROM 'C:\Users\laptop\Desktop\DW_generator\assessors.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Clients FROM 'C:\Users\laptop\Desktop\DW_generator\clients.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
      --, ROWTERMINATOR = '\r\n'
);

BULK INSERT dbo.Ownership FROM 'C:\Users\laptop\Desktop\DW_generator\ownership.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Insurances FROM 'C:\Users\laptop\Desktop\DW_generator\insurances.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);

BULK INSERT dbo.Claims FROM 'C:\Users\laptop\Desktop\DW_generator\claims.csv'
WITH ( CODEPAGE = '65001'
      , FORMAT = 'CSV'
      , FIRSTROW = 2
      , FIELDQUOTE = '\'
      , FIELDTERMINATOR = ','
--      , ROWTERMINATOR = '0x0a'
);
UPDATE SureSale.dbo.Clients
SET Voivodeship = 'NEW' WHERE ID = 1;

INSERT INTO SureSale.dbo.Claims VALUES (1000001, '2022-05-12', 0, 1063, '2022-05-12', 1, 0, 0, 2, 0, 2, 0, 0, 2, 1);

SELECT * FROM Car_Insurance.dbo.DT_Client WHERE PESEL = '85122897710';

SELECT * FROM Car_Insurance.dbo.FT_Claim WHERE ID_Client = 486538 or ID_Client = 581981;

DELETE FROM SureSale.dbo.Claims WHERE ID = 1000001;
USE SureSale
GO

UPDATE Clients
	SET City = 'Gdañsk'
	WHERE Voivodeship = 'Pomorskie'
;

UPDATE Clients
	SET Voivodeship = 'Mazowieckie'
	WHERE City = 'Warszawa'
;

INSERT INTO Claims VALUES
(1000009, '2021-05-09', '1', 15, '2021-05-13', 1, 1, 1, 2, 2, 0, 0, 0, 0, 3)
;
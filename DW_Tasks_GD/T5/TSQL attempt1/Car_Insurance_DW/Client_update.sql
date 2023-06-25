use SureSale
GO

UPDATE Clients
	SET Voivodeship = 'Pomorskie'
	WHERE City = 'Gdañsk' 
;

UPDATE Clients
	SET Voivodeship = 'Mazowieckie'
	WHERE City = 'Warszawa'
;

UPDATE Clients
	SET City = 'Poznañ', Voivodeship = 'Wielkopolskie'
	WHERE City = 'Warszawa'
;

-- run after INSERT
--UPDATE Clients
--	SET License_issuing_date = '1993-01-02'
--	WHERE PESEL = '12345678900'
--;
use SureSale
GO

UPDATE Clients
	SET Voivodeship = 'Pomorskie'
	WHERE City = 'Gda�sk' 
;

UPDATE Clients
	SET Voivodeship = 'Mazowieckie'
	WHERE City = 'Warszawa'
;

UPDATE Clients
	SET City = 'Pozna�', Voivodeship = 'Wielkopolskie'
	WHERE City = 'Warszawa'
;

-- run after INSERT
--UPDATE Clients
--	SET License_issuing_date = '1993-01-02'
--	WHERE PESEL = '12345678900'
--;
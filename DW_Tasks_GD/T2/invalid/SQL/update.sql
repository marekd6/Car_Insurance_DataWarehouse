use SureSale
GO

UPDATE Parts
	SET Value = 1210
	WHERE Part = 'Engine' AND Car_type_ID = 1
;

UPDATE Clients
	SET City = 'Gdañsk'
	WHERE Voivodeship = 'Pomorskie'
;

UPDATE Clients
	SET Voivodeship = 'Mazowieckie'
	WHERE City = 'Warszawa'
;

UPDATE Claims
	SET Indemnity = 555
	WHERE Assessor_ID % 2 = 0
;

UPDATE Claims
	SET Evaluation_date = Submission_date
	WHERE ID % 3 = 0
;

UPDATE Claims
	SET Indemnity = Indemnity*2
	WHERE Indemnity < 1000;
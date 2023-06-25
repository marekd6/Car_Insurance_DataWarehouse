use SureSale
GO

SELECT Clients.Surname, Insurances.ID, Insurances.Sale_date, Clients.ID
FROM Clients
JOIN Insurances ON Clients.ID = Insurances.Client_ID
;

SELECT Parts.Part, Parts.Value, Car_Types.Production_year
FROM Parts
JOIN Car_Types ON Car_Types.ID = Parts.Car_type_ID
;

SELECT Claims.Indemnity, Claims.Evaluation_date, Claims.Submission_date, Insurances.Sale_date, Insurances.Car, Clients.Surname
FROM Claims
JOIN Insurances ON Claims.Insurance_ID = Insurances.ID
JOIN Clients ON Clients.ID = Insurances.Client_ID
;
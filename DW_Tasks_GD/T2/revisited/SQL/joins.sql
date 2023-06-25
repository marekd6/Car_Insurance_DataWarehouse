use SureSale2
GO

SELECT Clients.Surname, Insurances.ID, Insurances.Sale_date, Clients.ID
FROM Clients
JOIN Insurances ON Clients.ID = Insurances.Client_ID
;

SELECT Claims.ID, Claims.Insurance_ID, Claims.Submission_date, Insurances.Sale_date, Insurances.Car_ID, Clients.Surname
FROM Claims
JOIN Insurances ON Claims.Insurance_ID = Insurances.ID
JOIN Clients ON Clients.ID = Insurances.Client_ID
ORDER BY Claims.ID
;
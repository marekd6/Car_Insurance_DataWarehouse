use Car_Insurance
go

-- Fill DT_Dates Lookup Table
-- Step a: Declare variables use in processing
Declare @StartDate date; 
Declare @EndDate date;

-- Step b:  Fill the variable with values for the range of years needed
SELECT @StartDate = '1993-01-01', @EndDate = '2022-12-31';

-- Step c:  Use a while loop to add dates to the table
Declare @DateInProcess datetime = @StartDate;

While @DateInProcess <= @EndDate
	Begin
	--Add a row into the date dimension table for this date
		Insert Into [dbo].[DT_Date] 
		( [Date]
		, [Year]
		, [Month]
		, [MonthNo]
		, [Day]
		)
		Values ( 
		  @DateInProcess -- [Date]
		  , Cast( Year(@DateInProcess) as varchar(4)) -- [Year]
		  , Cast( DATENAME(month, @DateInProcess) as varchar(10)) -- [Month]
		  , Cast( Month(@DateInProcess) as int) -- [MonthNo]
		  , Cast( Day(@DateInProcess) as int) -- [Day]
		);  
		-- Add a day and loop again
		Set @DateInProcess = DateAdd(d, 1, @DateInProcess);
	End
go

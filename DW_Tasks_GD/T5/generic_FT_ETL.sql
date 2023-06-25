--supplementary material resulting from participation in DW course 2023
--by Marek Drwal, 16.06.23

--a generic T-SQL code for loading Fact Table into Data Warehouse in ETL process;
--a star schema is considered;

--first, a view or a series of views is created;
--this view logically links data from sources (DB, CSVs, Excels, etc.)
--in order to create facts;
--it utilieses FT as a candidate Fact Table
--and other tables Ts as candidate Dimension Tables;
--JOINs link data from sources (DB, CSVs, Excels, etc.)
--using Business Keys
--in a way described in specifications;
--in effect, BKs and measures are selected;
--often, measures are generated in a series of calculations;
IF (object_id('measuresV') IS NOT NULL) DROP VIEW measuresV;
GO
CREATE VIEW measuresV AS --sources view
	SELECT
		val1, val2, val3, --measures
		BK1, BK2, BK3 --BKs
	FROM DB.FT --candidate FT from sources
	JOIN DB.Ta ON DB.Ta.BKa=DB.FT.BK1 --candidate DTs from sources
	JOIN DB.Tb ON DB.Tb.BKb=DB.FT.BK2
	JOIN CSV ON CSV.BKcsv=FT.BK3
;
GO

--then, another view providing PKs of Dimension Tables from the DW is generated;
--sources view is joined with DTs
--via Dimension BKs
--however, PKs from DTs are selected instead;
--when a BK from sources view is not specified in the DT
--then the Unknown tuple is selected;
--Unknown tuple is usually inserted into DTs at ID=-1;
IF (object_id('ETLv') IS NOT NULL) DROP VIEW ETLv;
GO
CREATE VIEW ETLv AS --warehouse view
	SELECT
		val1, val2, val3, --measures
		ID1=ISNULL(DT1.ID,-1), ID2=ISNULL(DT2.ID,-1), ID3=ISNULL(DT3.ID,-1) --IDs (surrogate keys) from DTs or the Unknown tuple ID
	FROM measuresV --sources view
	--a LEFT JOIN allowing to operate on all values from the sources view
	LEFT JOIN DW.DT1 ON DW.DT1.BK1=measuresV.BK1 --linking sources with the DW via BKs
	LEFT JOIN DW.DT2 ON DW.DT2.BK2=measuresV.BK2
	LEFT JOIN DW.DT3 ON DW.DT3.BK3=measuresV.BK3
	WHERE DW.DT1.Is_Current=1 --for SCD2 choose only up-to-date tuples
;
GO

--finally, a MERGE statement to insert new facts into the DW from warehouse view is issued;
--facts from the DW and from warehouse view are matched
--via IDs of dimensions,
--as the composition of PKs from dimensions constitutes PK of a fact;
--when a fact from the warehouse view is not found (NOT MATCHED) in the DW
--then it is inserted into the DW;
MERGE INTO DW.FT AS TT --DW FT as a target
	USING ETLv AS ST --warehouse view as a source
	ON TT.ID1=ST.ID1 --IDs as linkers
		AND TT.ID2=ST.ID2
		AND TT.ID3=ST.ID3
			WHEN NOT MATCHED
			THEN
				INSERT VALUES
					(ST.val1, ST.val2, ST.val3, --measures
					ST.ID1, ST.ID2, ST.ID3) --IDs
;
GO

DROP VIEW measuresV;
DROP VIEW ETLv;
GO
TEST CASE 1
- Load T1 snapshot to the source db/file.
- Run ETL.
- Check if the number of rows in fact tables corresponds to the number of related rows in the sources.
- Run ETL again and check if rows in the fact table were not duplicated (there is still the same number of facts and corresponding source rows).

TEST CASE 2
- Load T2 snapshot to the source db/file.
- Run ETL.
- Check if the number of rows in fact tables corresponds to the number of related rows in the sources.

TEST CASE 3
- Load T2 snapshot to the source db/file.
- Run ETL.
- Check if the new row is added to the SCD2 dimension.
- Check if the old row is updated (experiation date is added or isCurrent is set to 0).
- Run ETL once again and check if there was no change in the DW.

TEST CASE 4
- Update the entity in the source (e.g. education status for one Employee). This entity should be the one that is being loaded to the dimension with SCD2.
- Add new fact to the SOURCE that would refer to the updated entity (e.g. add new bill for the sale made by an Employee that has recently changed the education status)
- run ETL.
- Check if the new fact in DW is referring to the updated dimension row (e.g. sales fact refers to the employee with the updated education status)

TEST CASE 5
- Process the cube. See if it finishes without any errors.

TEST CASE 6
- Add new fact to the SOURCE that wouldn't refer to any entity from one chosen dimension (e.g. we don't know the sale date of one new bill)
- Run ETL.
- Check if 'UNKNOWN' row is being referred by this new fact in the DW.
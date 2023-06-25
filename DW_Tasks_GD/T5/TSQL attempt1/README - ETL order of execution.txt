! Note that for testing purposes the ETL_load_employee.sql script
has a parametrizable EntryDate (can be understood as ETL's current timestamp).
In the actual ETL this piece of code would not exist
and @EntryDate would be replaced by CURRENT_TIMESTAMP. !

-- stage1
load date; done; works
load unknown; done; works

-- stage2
load car; done; works
load assessor; done; works
load client; scd2; seems to be done and work

--stage3
load claim; csv

process the CUBE
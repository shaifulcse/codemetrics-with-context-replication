# codemetrics-with-context-data-for-replication
### Complexity and Change Data

The `info/settings-project.txt` file contains: project name checkoutDate  and snapshot for checkout (for all the 47 projects).

### Complexity and Change Data

The `data/complexity-and-change-data` directory contains measurements for all the 47 Java projects. 
The first line (header) shows the metrics' names (columns are separated by tab). For each metric measurement, there can be multiple values because we captured the complete evolution history of each method. 

McCabe values 5,6,7 means at the introduction (when the method was first pushed), the McCabe was 5. Then after a change, it became 6, and then 7 (latest).   

But for change values (such as ChangeDates), the first value is always 0. It means the method was introduced that day. The first value is 0 for other change indicators as well, because the method was introduced, not modified.  

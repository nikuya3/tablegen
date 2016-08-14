# tablegen
tablegen is a simple, lightweight Python script which converts a CSV table into a SQL CREATE TABLE statement.
## Setup
```
$ git clone https://github.com/nikuya3/tablegen
$ cd tablegen
$ ./tablegen.py
```
## How to use
Pass a file to the tablegen script and it will automatically output the CREATE TABLE statement.
```
$ ./tablegen test.csv
CREATE TABLE [file_name] ( [primary_col] [type] PRIMARY KEY, [col_header] [type], [col2_header] [type] );
```
### Options
|Shorthand|Long|Values|Description|
|---|---|---|---|
|-|file|file paths|The path to the CSV file|
|-p|--primary|number|The number of the primary column. Specify a number outside of the range of columns(eg. -1) to indicate that there is now primary column|
|-hr|--header|number|The number of the header row. Specify a number outside of the range of rows (eg. -1) to indicate that there is now header row|
|-d|--dbms|[psql,mysql,sqlite,server]|The targeted DBMS|
|-n|--name|string|The name of the table to be created. Leave blank to use file name|

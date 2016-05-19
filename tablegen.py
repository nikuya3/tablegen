import argparse
import csv
import codecs
import datetime
import os
from os.path import basename



parser = argparse.ArgumentParser(description='Generates an SQL CREATE TABLE statement from a CSV file', prog='tablegen')
parser.add_argument('file', type=str, help='The path to the CSV file.')
parser.add_argument('-p', '--primary', type=int, default=0, help='The number of the primary column. Specify a number outside of the range of'
                                         ' columns(eg. -1) to indicate that there is now primary column.')
parser.add_argument('-hr', '--header', type=int, default=0, help='The number of the header row. Specify a number outside of the range of rows'
                                         ' (eg. -1) to indicate that there is now header row.')
parser.add_argument('-d', '--dbms', type=str, default='psql', choices=['psql', 'mysql', 'sqlite', 'server'], help='''The targeted DBMS. Possible values:
                                                psql
                                                mysql
                                                sqlite
                                                server''')
args = parser.parse_args()
dbms = args.dbms
headerrow = args.header
filename = args.file
primarycol = args.primary
stmt = 'CREATE TABLE'

def is_integer(s):
    """Checks whether the given object is an integer.
    Args:
        s: The object to be checked.
    Returns:
        A boolean value indicating whether the given object is an integer.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s):
    """Checks whether the given object is a floating point value.
    Args:
        s: The object to be checked.
    Returns:
        A boolean value indicating whether the given object is a floating point value.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_boolean(s):
    """Checks whether the given object is a boolean value.
    Args:
        s: The object to be checked.
    Returns:
        A boolean value indicating whether the given object is an integer.
    """
    s = s.lower()
    return s == 'true' or s == 'false' or s == 'yes' or s == 'no'


def is_binary(s):
    """Checks whether the given object is a binary value.
    Args:
        s: The object to be checked.
    Returns:
        A boolean value indicating whether the given object is a binary value.
    """
    try:
        int(s, 2)
        return True
    except ValueError:
        return False


def is_date_time(s):
    pass


def get_col_sql_type(colnum):
    """Retrieves the SQL Datatype matching the values located in the columns of the given number.
    Args:
        colnum: The number of the column walues in each row.
    Returns:
        A string containing the SQL Datatype.
    """
    detected_binary = True
    detected_boolean = True
    detected_float = True
    detected_integer = True
    rownum = 0
    longest_value = 0
    for row in rows:
        if rownum == 0:
            rownum += 1
            continue
        num = 0
        for column in row:
            if num == colnum:
                if len(column) > 0:
                    if detected_binary:
                        detected_binary = is_binary(column)
                    if detected_boolean:
                        detected_boolean = is_binary(column)
                    if detected_float:
                        detected_float = is_float(column)
                    if detected_integer:
                        detected_integer = is_integer(column)
                    if longest_value < len(column):
                        longest_value = len(column)
            num += 1
        rownum += 1
    if detected_binary:
        return 'binary'
    if detected_boolean:
        return 'boolean'
    if detected_float and not detected_integer:
        return 'float'
    if detected_integer:
        return 'integer'
    return 'varchar(' + str(longest_value) + ')'


def interprete_header_row(row):
    cols = []
    for col in row:
        cols.append(col)
    if primarycol < 0 or primarycol > len(cols):
        stmt += 'id INTEGER PRIMARY KEY'
    colnum = 0
    for col in cols:
        stmt += ' ' + col
        stmt += ' ' + get_col_sql_type(colnum)
        # Process primary row
        if colnum == primarycol:
            stmt += ' PRIMARY KEY'
        stmt += ','
        colnum += 1


# Read CSV file with Unicode codec
with codecs.open(filename, 'r', 'utf-8') as csvfile:
    # Concatenate the statement with the filename without extension as table name
    stmt += ' ' + os.path.splitext(basename(filename))[0] + ' ('
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # Save rows in list
    rows = []
    for row in reader:
        rows.append(row)
    if headerrow < 0 or headerrow > len(rows):
        interprete_column(rows[0])
    # Interprete rows
    rownum = 0
    for row in rows:
        # Process header row
        if rownum == headerrow:
            interprete_header_row(row)
        rownum += 1
    # Remove the last space
    stmt = stmt[:-1]
    stmt += ');'
    print(stmt)
# tablegen pl.csv -p 1 -h no -d psql
# CREATE TABLE [file_name] ( [primary_col] [type] PRIMARY KEY, [col_header] [type], [col2_header] [type] );

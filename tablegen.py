import argparse
import csv
import codecs
import sys

stmt = 'CREATE TABLE'
primary_key = ''
reader = None

"""parser = argparse.ArgumentParser(description='Generates an SQL CREATE TABLE statement from a CSV file')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()

# Check arguments
for arg in sys.argv:
    print(arg)"""


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
    """Checks whether the given object is an integer.
    Args:
        s: The object to be checked.
    Returns:
        A boolean value indicating whether the given object is an integer.
    """
    try:
        int(s, 2)
        return True
    except ValueError:
        return False


def get_col_sql_type(colnum):
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
                        print(column + ',' + 'binary')
                        detected_binary = is_binary(column)
                    if detected_boolean:
                        print(column + ',' + 'boolean')
                        detected_boolean = is_binary(column)
                    if detected_float:
                        print(column + ',' + 'float')
                        detected_float = is_float(column)
                    if detected_integer:
                        print(column + ',' + 'integer')
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


# Read CSV file
filename = 'test.csv'
with codecs.open(filename, 'r', 'utf-8') as csvfile:
    stmt += ' ' + csvfile.name[:len(filename) - 4] + ' ('
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    rownum = 0
    rows = []
    for row in reader:
        rows.append(row)
    for row in rows:
        if rownum == 0:
            colnum = 0
            for col in row:
                stmt += ' ' + col
                stmt += ' ' + get_col_sql_type(colnum)
                if colnum == 0:
                    stmt += ' PRIMARY KEY'
                stmt += ','
                colnum += 1
        rownum += 1
    stmt = stmt[:-1]
    stmt += ');'
    print(stmt)
# tablegen test.csv -p 1 -h no -d psql
# CREATE TABLE [file_name] ( [primary_col] [type] PRIMARY KEY, [col_header] [type], [col2_header] [type] );

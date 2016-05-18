import argparse
import csv
import codecs
import sys

stmt = 'CREATE TABLE';
primary_key = ''
reader = None

parser = argparse.ArgumentParser(description='Generates an SQL CREATE TABLE statement from a CSV file')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()

# Check arguments
for arg in sys.argv:
    print(arg)


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_decimal(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_sql_type(colnum):
    decimal = False
    integer = False
    rownum = 0
    for row in reader:
        if rownum == 0:
            continue
        num = 0
        for col in row:
            if num == colnum:
                decimal = is_decimal(col)
            num += 1
        rownum += 1
    return 'varchar(80)'

# Read CSV file
filename = 'test.csv'
with codecs.open(filename, 'r', 'utf-8') as csvfile:
    stmt += ' ' + csvfile.name[:len(filename) - 4] + ' ('
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    rownum = 0
    for row in reader:
        if rownum == 0:
            colnum = 0
            for col in row:
                stmt += ' ' + col
                stmt += ' ' + get_sql_type(col)
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

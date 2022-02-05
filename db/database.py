import psycopg2
import psycopg2.extras
import os

class Connection:
  def __init__(self, db_name):
    self.con = psycopg2.connect(database=db_name,
                                user='postgres',
                                password='postgres',
                                host=os.getenv('DB_HOST'),
                                port="5432")

  def close(self):
    self.close()

class Query:
  def __init__(self):
    self.connection = Connection('oss_repositories')
    self.cursor = self.connection.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  def execute(self, sql):
    self.cursor.execute(sql)
  
  def query(self, sql):
    self.execute(sql)
    results = []
    for row in self.cursor.fetchall():
      results.append(row)
    return results

  def get(self, table, column=None, value=None, columns=[]):
    select_columns = '*' if len(columns) == 0 else ', '.join(columns)
    if type(value) == str:
      value = f"'{value}'"
    if value:
      query_string = f'SELECT {select_columns} FROM  {table} WHERE {column} = {value}'
    else:
      query_string = f'SELECT {select_columns} FROM {table}'
    return self.query(query_string)

  def command(self, sql):
    cursor = self.connection.con.cursor()
    cursor.execute(sql)
    self.connection.con.commit()
  
  def insert(self, table, columns, values):
    column_string = f"({', '.join(columns)})"
    # Must stringify the numeric values for this join
    stringy_list = []
    for value in values:
      stringy_list.append(str(value))
    value_string = f"({', '.join(stringy_list)})"
    query_string = f"INSERT INTO {table} {column_string} VALUES {value_string};"
    self.command(query_string)

  def update(self, table, column, new_value, where, matcher):
    # UPDATE table SET column = new_value WHERE where = matcher
    if type(new_value) == str:
      new_value = f"{new_value}"
    query_string = f'UPDATE {table} SET {column} = {new_value} WHERE {where} = {matcher}'
    self.command(query_string)

from db.database import Query

class Entity:
  def __init__(self, table_name):
      self._table_name = table_name

  @property
  def table_name(self):
    return self._table_name
  
  @table_name.setter
  def table_name(self, _value):
    # Don't let table name change
    pass

  def column_list(self):
    raise NotImplementedError
  
  def values_list(self):
    raise NotImplementedError
  
  def sql_friendly_values(self):
    # For use in bulk inserts
    stringy_list = []
    for value in self.values_list:
      stringy_list.append(str(value))
    return ', '.join(stringy_list)
  
  def write_to_database(self):
    """
    This method writes the entity's data to the
    database, but preferably we'd use the Query class's
    bulk_insert method after building a list of these
    classes. This is kind of a "just-in-case" method.
    """
    q = Query()
    q.insert(self.table_name, self.column_list, self.values_list)
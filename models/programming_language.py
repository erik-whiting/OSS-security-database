from db.database import Query
from models.entity import Entity

class ProgrammingLanguage(Entity):
  """
  This class captures some metadata of a language so
  we can keep track of a repository's specific needs
  as far as building its CodeQL database
  """
  def __init__(self, id, name, compiled):
    super().__init__('programming_languages')
    self.id = id
    self.name = name
    self.compiled = compiled
  
  @property
  def column_list(self):
    return [
      'id',
      'name',
      'compiled'
    ]

  @property
  def values_list(self):
    return [
      self.id,
      self.name,
      self.compiled
    ]

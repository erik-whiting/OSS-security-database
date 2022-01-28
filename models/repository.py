from db.database import Query

class Repository:
  """
  This is a class for instantiating objects representing
  repositories that were returned from the API query
  in RepoQuery. The query returns a lot of data that
  we don't need, so this class encapsualtes the important
  data points.
  """

  TABLE_NAME='repositories'

  def __init__(self, repo_object, programming_language):
    # We explicitly write the ID because we're using its GitHub ID
    self.id = repo_object.id
    self.name = repo_object.name
    self.html_url = repo_object.html_url
    self.clone_url = repo_object.clone_url
    self.ssh_url = repo_object.ssh_url
    self.git_url = repo_object.git_url
    self.topics = ','.join(repo_object.get_topics())
    self.stars = repo_object.stargazers_count
    self.forks = repo_object.forks_count
    self.watchers = repo_object.watchers_count
    self.programming_language = programming_language
  
  @staticmethod
  def column_list():
    return [
      'id',
      'name',
      'html_url',
      'clone_url',
      'ssh_url',
      'git_url',
      'topics',
      'stars',
      'forks',
      'watchers',
      'programming_language'
    ]

  def values_list(self):
    return [
      self.id,
      self.name,
      self.html_url,
      self.clone_url,
      self.ssh_url,
      self.git_url,
      self.topics,
      self.stars,
      self.forks,
      self.watchers,
      self.programming_language
    ]
  
  def values_dict(self):
    vdict = {}
    index = 0
    for value in self.column_list():
      vdict[value] = self.values_list()[index]
      index += 1
    return vdict
  
  def sql_friendly_insert_values(self):
    db_string_columns = [
      'name',
      'html_url',
      'clone_url',
      'ssh_url',
      'git_url',
      'topics',
      'programming_language'
    ]

    retvals = []
    for column in self.values_dict().keys():
      if column in db_string_columns:
        sql_insert_value = f"'{self.values_dict()[column]}'"
        retvals.append(sql_insert_value)    
      else:
        retvals.append(str(self.values_dict()[column]))
    return retvals

  
  def sql_friendly_values(self):
    return ', '.join(self.sql_friendly_insert_values())

  def write_to_database(self):
    """
    This method writes the repository's data to the
    database, but preferably we'd use the Query class's
    bulk_insert method after building a list of these
    classes. This is kind of a "just-in-case" method.
    """
    q = Query()
    q.insert('repositories', self.column_list(), self.sql_friendly_insert_values())
    
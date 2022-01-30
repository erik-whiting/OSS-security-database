from db.database import Query

class RepositoryData:
  """
  This is a class for instantiating objects representing
  repositories that were returned from the API query
  in RepoQuery. The query returns a lot of data that
  we don't need, so this class encapsualtes the important
  data points.
  """

  def __init__(self, repo_object, programming_language):
    # We explicitly write the ID because we're using its GitHub ID
    self.id = repo_object.id
    self.name = repo_object.name
    self.description = repo_object.description
    self.latest_recorded_commit = repo_object.get_commits()[0].sha
    self.html_url = repo_object.html_url
    self.clone_url = repo_object.clone_url
    self.ssh_url = repo_object.ssh_url
    self.git_url = repo_object.git_url
    self.topics = ','.join(repo_object.get_topics())
    self.stars = repo_object.stargazers_count
    self.forks = repo_object.forks_count
    self.watchers = repo_object.watchers_count
    self.issues = repo_object.open_issues_count
    self.programming_language = programming_language
    self.created = repo_object.created_at
  
  @staticmethod
  def column_list():
    return [
      'id',
      'name',
      'description',
      'latest_recorded_commit',
      'html_url',
      'clone_url',
      'ssh_url',
      'git_url',
      'topics',
      'stars',
      'forks',
      'watchers',
      'issues',
      'programming_language',
      'created'
    ]

  def values_list(self):
    return [
      self.id,
      self.name,
      self.description,
      self.latest_recorded_commit,
      self.html_url,
      self.clone_url,
      self.ssh_url,
      self.git_url,
      self.topics,
      self.stars,
      self.forks,
      self.watchers,
      self.issues,
      self.programming_language,
      self.created
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
      'description',
      'latest_recorded_commit',
      'html_url',
      'clone_url',
      'ssh_url',
      'git_url',
      'topics',
      'stars',
      'forks',
      'watchers',
      'issues',
      'programming_language',
      'created'
    ]

    retvals = []
    for column in self.values_dict().keys():
      if column in db_string_columns:
        insert_value = self.values_dict()[column]
        psql_insert_value = self.postgres_friendly_insert_values(insert_value)
        sql_insert_value = f"'{psql_insert_value}'"
        retvals.append(sql_insert_value)
      else:
        retvals.append(str(self.values_dict()[column]))
    return retvals

  def postgres_friendly_insert_values(self, value):
    if type(value) == str:
      return value.replace('\'', '\'\'')
    else:
      return value
  
  def sql_friendly_values(self):
    return ', '.join(self.sql_friendly_insert_values())

  def write_to_database(self):
    """
    This method writes the repository's data to the
    database. Unfortunately, we're doing this one
    repository at a time to ensure data integrity
    and to act accordingly if for some reason the
    write fails.
    """
    q = Query()
    # Check if we already inserted this
    already_exists = len(q.get('repositories', 'id', self.values_dict()['id'])) > 0
    if already_exists:
      print('This repository has already been inserted')
      raise RepoAlreadyExists
    else:
      try:
        q.insert('repositories', self.column_list(), self.sql_friendly_insert_values())
      except Exception as ex:
        raise ex
      return True

class RepoAlreadyExists(Exception):
  pass

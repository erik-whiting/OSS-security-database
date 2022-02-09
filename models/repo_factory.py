from db.database import Query
from models.repository import Repository

class RepoFactory:
  columns = [
    'id',
    'name',
    'latest_recorded_commit',
    'html_url',
    'clone_url',
    'ssh_url',
    'git_url',
    'programming_language'
  ]

  @staticmethod
  def find_by(column, value):
    data = RepoFactory.select_where(column, value)
    return Repository(data)

  @staticmethod
  def select_where(column, value):
    q = Query()
    repo_rows = q.get(
      'repositories',
      column=column,
      value=value,
      columns=RepoFactory.columns
    )
    if len(repo_rows) == 0:
      raise NoRepoFound
    elif len(repo_rows) > 1:
      raise MultipleReposFound
    else:
      repo_rows = repo_rows[0] # because Query.get retunrs a list of lists
    values_dict = {
      'id': repo_rows[0],
      'name': repo_rows[1],
      'latest_recorded_commit': repo_rows[2],
      'html_url': repo_rows[3],
      'clone_url': repo_rows[4],
      'ssh_url': repo_rows[5],
      'git_url': repo_rows[6],
      'programming_language': repo_rows[7]
    }
    values_dict['topics'] = RepoFactory.get_topics_by_id(values_dict['id'])
    return values_dict
  
  @staticmethod
  def get_topics_by_id(id):
    q = Query()
    topics = q.get(
      'repo_topics', 
      column='repository_id', 
      value=id,
      columns=['topic']
    )
    # This returns a list of lists, so we'll
    # flatten for easier data manipulation
    flat_topics = [t for topic in topics for t in topic]
    return flat_topics


class NoRepoFound(Exception):
  pass

class MultipleReposFound(Exception):
  pass

import os
from github import Github

from db.database import Query
from models.repository import Repository

class PrototypeQuery:
  def __init__(self):
    self.api = Github('erik-whiting', os.getenv('GH_PASS'))
  
  def get_repo_by_name(self, repo_name='erik-whiting/LuluTest'):
    gh_repo = self.api.get_repo(repo_name, lazy=False)
    repository = Repository(gh_repo, 'python')
    return repository

pq = PrototypeQuery()
repo = pq.get_repo_by_name()
q = Query()

table = 'repositories'
columns = repo.column_list()
values = [repo.sql_friendly_values()]

# q.bulk_insert(table, columns, values)

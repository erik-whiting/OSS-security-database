from time import sleep
import os

from github import Github, RateLimitExceededException
from db.database import Query
from models.repository import Repository

class RepoQuery:
  
  def __init__(self, token):
    self.api = Github(token)
    self.supported_languages =  [
      'c',
      'c++',
      'c#',
      'go',
      'java',
      'javascript',
      'python',
      'typescript'
    ] # skipping ruby because it's experimental

  def get_popular_repos_for(self, language):
    query_string = f'language:{language}'
    repos = self.api.search_repositories(
      query=query_string,
      sort='stars'
    )
    return repos
  
  def save_to_db(self, language, max_repos, bulk=True):
    if bulk:
      self.bulk_save_repos_to_db(language, max_repos)
    else:
      self.save_repos_to_db(language, max_repos)
  
  def save_repos_to_db(self, language, max_repos):
    gh_repositories = self.get_popular_repos_for(language)
    count = 0
    for gh_repository in gh_repositories:
      if count > max_repos:
        break
      if gh_repository.archived:
        continue
      repo = Repository(gh_repository, language)
      count += 1
      print(f"Writing {repo.name} to database ... ")
      repo.write_to_database()
      print("Sleeping for 1 second (avoiding rate limit)")
      sleep(1)

  def bulk_save_repos_to_db(self, language, max_repos):
    gh_repositories = self.get_popular_repos_for(language)
    count = 0
    insert_values = []
    for gh_repository in gh_repositories:
      if count > max_repos:
        break
      if gh_repository.archived:
        continue
      repo = Repository(gh_repository, language)
      insert_values.append(repo.sql_friendly_values())
      count += 1
    q = Query()
    columns = Repository.column_list()
    q.bulk_insert('repositories', columns, insert_values)

  def build_database(self, max_repos_per_language, bulk=True):
    for language in self.supported_languages:
      self.save_to_db(language, max_repos_per_language, bulk)
    

token = ''
with open('.tmp/gh_token_maybe.txt') as f:
  token = f.read()

rq = RepoQuery(token)
rq.build_database(20, False)

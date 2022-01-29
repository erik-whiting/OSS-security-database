from time import sleep
import os

from github import Github
from models.repository_data import RepositoryData

gh_user = 'erik-whiting'
gh_token = os.getenv('gh_token')

def get_repo_objects(api, language):
  print(f'Beginning query of {language} repositories')
  print(f'Sleeping for 5 seconds just because')
  print(f'{api.rate_limiting[0]} calls left this hour')
  print(f'Rate limit will reset at {api.rate_limiting_resettime}')
  sleep(5)
  query_string = f'language:{language}'
  repos = api.search_repositories(
    query=query_string,
    sort='stars'
  )
  return repos

def write_repo_to_db(api, language, max_repos):
  count = 0
  # this next three variables are for
  # preventing reaching a rate limit
  calls_since_last_pause = 0
  when_to_pause = 20
  pause_duration = 2

  repo_objects = get_repo_objects(api, language)
  for repo_object in repo_objects:
    if count >= max_repos:
      break
    if repo_object.archived:
      # Repository is archived and
      # therefore we don't want to
      # included it for further analysis.
      continue
    repo = RepositoryData(repo_object, language)
    api_calls_remaining = api.rate_limiting[0]
    while api_calls_remaining <= 100:
      sleep(5 * 60) # wait five minutes to reset rate limit
    calls_since_last_pause += 1 # Because we've made one API request
    if calls_since_last_pause >= when_to_pause:
      calls_since_last_pause = 0
      print(f'Sleeping for {pause_duration} second(s) to avoid rate limiting')
      print(f'(we can make {api_calls_remaining} more calls until it resets)')
      sleep(pause_duration)

    print(f'Writing {repo.name} to databse (number {count + 1} for {language})')
    if repo.write_to_database():
      print(f'Successfully wrote {repo.name} to database')
      count += 1
    else:
      print(f'Failed to write {repo.name}, continuing ... ')
    

supported_languages = [
  'c',
  'c++',
  'c#',
  'go',
  'java',
  'javascript',
  'python',
  'typescript'
] # skipping ruby because it's experimental

api = Github(gh_user, gh_token)
repos_per_language = 10
for language in supported_languages:
  write_repo_to_db(api, language, repos_per_language)

from time import sleep, time
from datetime import datetime
import os

from github import Github
from models.repository_data import RepoAlreadyExists, RepositoryData

gh_user = 'erik-whiting'
gh_token = os.getenv('gh_token')

def get_repo_objects(api, language):
  print('\n')
  print(f'Beginning query of {language} repositories')
  print(f'Sleeping for 5 seconds just because')
  print(f'{api.rate_limiting[0]} calls left this hour')
  print(f'Rate limit will reset at {api.rate_limiting_resettime}')
  print('\n')
  sleep(5)
  query_string = f'language:{language}'
  repos = api.search_repositories(
    query=query_string,
    sort='stars'
  )
  return repos

def write_repo_to_db(api, language, max_repos):
  count = 0
  # these next three variables are for
  # preventing reaching a rate limit
  calls_since_last_pause = 0
  when_to_pause = 20
  pause_duration = 2

  # Create new error log
  f = open('repo_error_log.csv', 'w')
  f.write('error_typ,repo_name,repo_id,time\n')
  f.close()

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
    if get_remaining_api_calls(api) <= 100:
      sleep_until_rate_limit_resets(api)

    calls_since_last_pause += 1 # Because we've made one API request
    if calls_since_last_pause >= when_to_pause:
      calls_since_last_pause = 0
      print(f'Sleeping for {pause_duration} second(s) to avoid rate limiting')
      print(f'(we can make {get_remaining_api_calls(api)} more calls until it resets)')
      sleep(pause_duration)

    print(f'Writing {repo.name} to databse (number {count + 1} for {language})')
    try:
      success = repo.write_to_database()
    except RepoAlreadyExists:
      success = False
      log_error('already_exists', repo.name, repo.id)
    except Exception as ex:
      success = False
      log_error(ex, repo.name, repo.id)

    if success:
      print(f'Successfully wrote {repo.name} to database')
      count += 1
    else:
      print(f'Failed to write {repo.name}, writing error message ... ')

def sleep_until_rate_limit_resets(api):
  seconds_until_reset = int(api.rate_limiting_resettime - time())
  seconds_until_reset += 30 # just to be safe
  now = time()
  formatted_now = datetime.utcfromtimestamp(now).strftime('%H:%M:%S on %Y-%m-%d')
  reset_time = now + seconds_until_reset
  formatted_reset_time = datetime.utcfromtimestamp(reset_time).strftime('%H:%M:%S on %Y-%m-%d')
  print('\n')
  print(f'This message was printed at {formatted_now}')
  print(f'Sleeping for approximately {int(seconds_until_reset / 60) + 1} minutes to avoid rate limiting')
  print(f'Scheduled to start again at {formatted_reset_time}')
  print('\n')
  sleep(seconds_until_reset)

def log_error(error_type, repo_name, repo_id):
  error_message = f'{error_type},{repo_name},{repo_id},{time()}\n\n'
  f = open('error_log.csv', 'a')
  f.write(error_message)
  f.close()

def get_remaining_api_calls(api):
  return api.rate_limiting[0]

languages_to_query = ['javascript', 'typescript']

api = Github(gh_user, gh_token)
repos_per_language = 500
for language in languages_to_query:
  write_repo_to_db(api, language, repos_per_language)

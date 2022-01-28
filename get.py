from time import sleep
import os

from github import Github, RateLimitExceededException

SUPPORTED_LANGUAGES = [
  'c',
  'c++',
  'c#',
  'go',
  'java',
  'javascript',
  'python',
  'typescript'
] # skipping ruby because it's experimental

# Here's the basic idea:

gh_user = 'erik-whiting'
gh_password = os.getenv('GH_PASS')
test_lang = SUPPORTED_LANGUAGES[0]

api = Github('erik-whiting', password=gh_password) # you can add a kwarg too
# make a generator:
repos = api.search_repositories(query=f'language:{test_lang}')

### Still figuring it out from here

for language in SUPPORTED_LANGUAGES:
  print(language)

def get_popular_repos_for(language):
  pass
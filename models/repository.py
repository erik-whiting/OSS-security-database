from subprocess import Popen, PIPE
import os

class Repository:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.latest_recorded_commit = data['latest_recorded_commit']
    self.html_url = data['html_url']
    self.clone_url = data['clone_url']
    self.ssh_url = data['ssh_url']
    self.git_url = data['git_url']
    self.topics = data['topics']
    self.language = data['programming_language']
  
  def git_clone_string(self, from_url=None):
    url = self.clone_url
    if from_url == 'ssh':
      url = self.ssh_url
    elif from_url == 'git':
      url = self.git_url
    string = f'git clone {url} ./cloned_repositories/{self.id}/{self.name}'
    return string

  def clone(self, from_url=None):
    try:
      os.mkdir('./cloned_repositories')
    except FileExistsError:
      print('cloned_repositories exists, moving on')
    
    try:
      os.mkdir(f'./cloned_repositories/{self.id}')
    except FileExistsError:
      print(f'./cloned_repositories/{self.id} exists, moving on')
    
    try:
      os.mkdir(f'./cloned_repositories/{self.id}/{self.name}')
    except FileExistsError:
      print(f'./cloned_repositories/{self.id}/{self.name} exists, moving on')
    os.system(self.git_clone_string(from_url))
  
  def verify_latest(self):
    command = Popen(
      [
        'git', 
        '-C', 
        f'./cloned_repositories/{self.id}/{self.name}', 
        'rev-parse', 
        'HEAD'
      ],
      stdout=PIPE
    )
    byte_hash = command.communicate()[0]
    local_commit = byte_hash.decode('utf-8')
    return local_commit == self.latest_recorded_commit

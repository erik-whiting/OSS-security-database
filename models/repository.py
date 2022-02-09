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
    # Check to see if the latest commit we have
    # in the database is the latest commit we
    # have now. The repository may have been
    # updated between putting its information
    # in the database and cloning it.
    command = Popen(
      [
        'git', 
        '-C', 
        f'./cloned_repositories/{self.id}/{self.name}', 
        'rev-parse', 
        'HEAD'
      ],
      stdout=PIPE # This is so we can get the return value
    )
    byte_hash = command.communicate()[0]
    local_commit = byte_hash.decode('utf-8')
    return local_commit == self.latest_recorded_commit
  
  def cql_extractor(self):
    if self.language == 'typescript':
      # The TS extractor is called 'javascript'
      return 'javascript'
    else:
      return self.language

  def source_root(self):
    return f'./cloned_repositories/{self.id}/{self.name}'
  
  def cql_database_path(self):
    return f'./code_ql_databases/{self.id}/{self.name}'
  
  def db_analysis_path(self):
    return f'./analysis_results/{self.id}/{self.name}/analysis.csv'
  
  def build_cql_database(self):
    try:
      os.mkdir(f'./code_ql_databases/')
    except FileExistsError:
      print('code_ql_databases already exists, moving on')
    try:
      os.mkdir(f'./code_ql_databases/{self.id}')
    except FileExistsError:
      print(f'./code_ql_databases/{self.id} already exists, moving on')
    
    command = Popen(
      [
        'codeql',
        'database',
        'create',
        self.cql_database_path(),
        f'--source-root={self.source_root()}',
        f'--language={self.cql_extractor()}'
      ],
      stdout=PIPE
    )
    return command.communicate()
  
  def analyze_cql_database(self):
    try:
      os.mkdir(f'./analysis_results/')
    except FileExistsError:
      print('analysis_results already exists, moving on')
    try:
      os.mkdir(f'./analysis_results/{self.id}')
    except FileExistsError:
      print(f'./analysis_results/{self.id} already exists, moving on')
    try:
      os.mkdir(f'./analysis_results/{self.id}/{self.name}')
    except FileExistsError:
      print(f'./analysis_results/{self.id}/{self.name} already exists, moving on')
    
    command = Popen(
      [
        'codeql',
        'database',
        'analyze',
        self.cql_database_path(),
        '--format=csv',
        f'--output={self.db_analysis_path()}',
        '--threads=0'
      ],
      stdout=PIPE
    )
    return command.communicate()

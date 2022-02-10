from subprocess import Popen, PIPE
import os, csv, shutil, errno, stat

from models.repo_vulnerability import RepoVulnerability

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
  
  def cleanup(self):
    # Since the system is going to evaluate
    # thousands of repositories, it's a good
    # idea to delete files when we're done
    # with them. Space is cheap but finite.

    repo_path = f'./cloned_repositories/{self.id}/{self.name}'
    code_ql_path = f'./code_ql_databases/{self.id}/{self.name}'
    analysis_path = f'./analysis_results/{self.id}/{self.name}'

    for path in [repo_path, code_ql_path, analysis_path]:
      full_path = os.path.abspath(path)
      shutil.rmtree(full_path, ignore_errors=False, onerror=self.remove_read_only)

  def verify_latest(self):
    # Check to see if the latest commit we have
    # in the database is the latest commit we
    # have now. The repository may have been
    # updated between putting its information
    # in the database and cloning it.
    local_commit = self.get_latest_commit()
    return local_commit == self.latest_recorded_commit
  
  def get_latest_commit(self):
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
    return byte_hash.decode('utf-8').strip()

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

  def get_vulnerabilities(self):
    analysis_location = f'./analysis_results/{self.id}/{self.name}/analysis.csv'
    retval = []
    with open(analysis_location, 'r', newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        retval.append(row[0])
    return retval

  def insert_vulnerabilities(self):
    vulnerabilities = self.get_vulnerabilities()
    for v in vulnerabilities:
      rv = RepoVulnerability(self, v)
      rv.insert()

  def remove_read_only(self, func, path, exc):
    # This method is for when shutil's rmtree
    # fails because permission is denied. This
    # script was taken from https://stackoverflow.com/a/1214935/11903505
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise

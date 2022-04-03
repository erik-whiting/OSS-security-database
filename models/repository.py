from subprocess import Popen, PIPE
import os, shutil, errno, stat

from db.database import Query
from models.repo_vulnerability import RepoVulnerability

class Repository:
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.html_url = data['html_url']
    self.clone_url = data['clone_url']
    self.ssh_url = data['ssh_url']
    self.git_url = data['git_url']
    self.topics = data['topics']
    self.language = data['programming_language']
    self.ram_setting = 1000 * 12

  def git_clone_string(self, from_url=None):
    url = self.clone_url
    if from_url == 'ssh':
      url = self.ssh_url
    elif from_url == 'git':
      url = self.git_url
    string = f'git clone {url} ./cloned_repositories/{self.id}/{self.name}'
    return string

  def mkdir(self, dir):
    if not os.path.isdir(dir):
      os.mkdir(dir)

  def directory_path_for(self, base):
    return [
      f'./{base}',
      f'./{base}/{self.id}',
      f'./{base}/{self.id}/{self.name}'
    ]

  def clone(self, from_url=None):
    for dir in self.directory_path_for('cloned_repositories'):
      self.mkdir(dir)
    os.system(self.git_clone_string(from_url))

  def cleanup(self):
    # Since the system is going to evaluate
    # thousands of repositories, it's a good
    # idea to delete files when we're done
    # with them. Space is cheap but finite.

    paths = [
      self.source_root(),
      self.cql_database_path(),
      f'./analysis_results/{self.id}/{self.name}'
    ]
    for path in paths:
      full_path = os.path.abspath(path)
      shutil.rmtree(full_path, ignore_errors=False, onerror=self.remove_read_only)

  def get_latest_commit(self):
    command = Popen(
      [
        'git',
        '-C',
        self.source_root(),
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
    self.mkdir('code_ql_databases')
    self.mkdir(f'./code_ql_databases/{self.id}')

    command = Popen(
      [
        'codeql',
        'database',
        'create',
        self.cql_database_path(),
        f'--source-root={self.source_root()}',
        f'--language={self.cql_extractor()}',
        '--threads=0',
        f'--ram={self.ram_setting}'
      ],
      stdout=PIPE
    )
    return command.communicate()

  def analyze_cql_database(self):
    for dir in self.directory_path_for('analysis_results'):
      self.mkdir(dir)

    command = Popen(
      [
        'codeql',
        'database',
        'analyze',
        self.cql_database_path(),
        '--format=csv',
        f'--output={self.db_analysis_path()}',
        '--threads=0',
        f'--ram={self.ram_setting}'
      ],
      stdout=PIPE
    )
    return command.communicate()

  def get_vulnerabilities(self):
    analysis_location = f'./analysis_results/{self.id}/{self.name}/analysis.csv'
    retval = []
    try:
      file = open(analysis_location)
      for line in file.readlines():
        vulnerability_name = line.split(',')[0].strip()
        retval.append(vulnerability_name)
    except Exception as e:
      print(f'Error occured getting vulnerabilities for {self.name}')
      print(f'Error message: f{e}')
      return False
    return retval

  def insert_vulnerabilities(self, analysis_id):
    vulnerabilities = self.get_vulnerabilities()
    if vulnerabilities == []:
      print('No vulnerabilities found')
      return True
    elif vulnerabilities:
      for v in vulnerabilities:
        rv = RepoVulnerability(self, v)
        rv.insert(analysis_id)
      return True
    else:
      return False

  def mark_analysis_completed(self, analysis_id):
    q = Query()
    update_completed = "completed = true"
    update_repo_head = f"repo_head = '{self.get_latest_commit()}'"
    where = f'repository_id = {self.id} AND analysis_id = {analysis_id}'
    sql = f'UPDATE analysis_repo SET {update_completed}, {update_repo_head} WHERE {where}'
    q.command(sql)

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

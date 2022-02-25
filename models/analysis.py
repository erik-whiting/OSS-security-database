from subprocess import Popen, PIPE
import datetime, os, shutil

from db.database import Query
from models.repo_factory import RepoFactory

class Analysis:
  def __init__(self, languages=[], topics=[]):
    self.id = None
    self.repo_ids = []
    self.prepared = False
    self.clauses = {
      'languages': languages if type(languages) == list else [languages]
    } # Should I add a topics clause?
    self.completed = False
    self.build_query()

  def prepare(self):
    q = Query()
    repo_ids = q.query(self.query)
    # Flatten list
    ids = [r for repo_id in repo_ids for r in repo_id]
    self.insert_self()
    for repo_id in ids:
      q.insert(
        'analysis_repo',
        ['analysis_id', 'repository_id'],
        [self.id, repo_id]
      )

    self.repo_ids = list(dict.fromkeys(ids)) # Remove duplicates
    directories = ['cloned_repositories', 'code_ql_databases', 'analysis_results']
    for directory in directories:
      try:
        os.mkdir(f'./{directory}')
      except FileExistsError:
        print(f'{directory} already exists')

    for repo_id in self.repo_ids:
      for directory in directories:
        try:
          os.mkdir(f'./{directory}/{id}')
        except FileExistsError:
          print(f'./{directory}/{id} already exists')

    self.prepared = True

  def insert_self(self):
    q = Query()
    insertable_query = self.query.replace('\'', '\'\'')
    columns = '(repo_extraction_sql, hash_of_codeql_repo, codeql_version)'
    values = f"('{insertable_query}', '{self.get_codeql_repo_hash()}', '{self.get_codeql_version()}')"
    sql = f"INSERT INTO analyses {columns} VALUES {values} RETURNING id"
    self.id = q.query(sql)[0][0]
    q.connection.con.commit()

  def get_codeql_version(self):
    command = Popen(
      [
        'codeql',
        'version',
        '--format=terse'
      ],
      stdout=PIPE
    )
    byte_hash = command.communicate()[0]
    return byte_hash.decode('utf-8').strip()

  def get_codeql_repo_hash(self):
    cql_binary = shutil.which('codeql')
    cql_home = os.path.dirname(os.path.dirname(cql_binary))
    cql_repo = os.path.join(cql_home, 'codeql-repo')
    command = Popen(
      [
        'git',
        '-C',
        cql_repo,
        'rev-parse',
        'HEAD'
      ],
      stdout=PIPE
    )
    byte_hash = command.communicate()[0]
    return byte_hash.decode('utf-8').strip()

  def build_query(self):
    sql = 'SELECT id FROM repositories'
    if self.clauses['languages']:
      sql += f' {self.language_clause()}'
    self.query = sql

  def language_clause(self):
    sql_friendly_langauges = "', '".join(self.clauses['languages'])
    sql_friendly_langauges = f"('{sql_friendly_langauges}')"
    return f'WHERE programming_language IN {sql_friendly_langauges}'

  def topic_clause(self):
    sql_friendly_topics = '%|%'.join(self.clauses['topics'])
    sql_friendly_topics = f"'%{sql_friendly_topics}%'"
    return f'WHERE lower(topics) SIMILAR TO lower({sql_friendly_topics})'

  def analyze_repositories(self):
    if not self.prepared:
      print('This analysis has not been prepared')
      print('Did you meant to run the Analysis#prepare method?')

    start_time = datetime.datetime.now()
    to_be_analyzed = len(self.repo_ids)
    print(f'Starting at {start_time}')
    print(f'There are {to_be_analyzed} repositories to analyzed')
    print(f'This may take hours, keep an eye out\n')
    repos_analyzed = 0
    for repo_id in self.repo_ids:
      print(f'\n{repos_analyzed} repositories analyzed')
      print(f'{to_be_analyzed - repos_analyzed} remaining')
      self.analyze_repo(repo_id)
      repos_analyzed += 1
    print(f'Analysis began at {start_time} and ended at {self.timestamp()}')

  def analyze_repo(self, repo_id):
    repo = RepoFactory.find_by('id', repo_id)
    print(f'{self.timestamp()} Cloning {repo.name} ...\n')
    repo.clone()
    print(f'{self.timestamp()} Building CQL database ...\n')
    repo.build_cql_database()
    print(f'{self.timestamp()} Beginning analysis of CQL database for {repo.name} ...\n')
    repo.analyze_cql_database()
    print(f'{self.timestamp()} Inserting {repo.name} vulnerabilities into database ...\n')
    if repo.insert_vulnerabilities(self.id):
      print('Insert successful')
      repo.mark_analysis_completed(self.id)
    else:
      print(f'Insertion of {repo.name} vulnerabilities failed\n')
    print(f'{self.timestamp()} Removing {repo.name} files ...\n')
    repo.cleanup()

  def restart_analysis(self):
    q = Query()
    sql = f'SELECT repository_id FROM analysis_repo WHERE NOT completed AND analysis_id = {self.id}'
    repo_ids = q.query(sql)
    # Flatten list
    ids = [r for repo_id in repo_ids for r in repo_id]
    self.repo_ids = ids
    print(f'Restarting analysis {self.id}')
    self.analyze_repositories()

  def timestamp(self):
    now = datetime.datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    return f'[{current_time}]'

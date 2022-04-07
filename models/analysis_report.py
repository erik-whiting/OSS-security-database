import pickle
from datetime import datetime

from models.analysis_factory import AnalysisFactory
from models.analysis import Analysis
from db.database import Query

class AnalysisReport:
  """
  This class exists to generate a report of the data
  generated from the Analysis class. The report should
  have enough data to reproduce the data generated
  by the Analysis class.
  """
  def __init__(self, analysis_id):
    self.analysis = AnalysisFactory.find(analysis_id)
    self.data = self.get_report_data()
    self.unanalyzed_repos = self.analysis.get_unanalyzed_ids()
    self.vulnerability_data = self.vulnerabilities_found()
    self.summary = self.summarize_data()

  def __eq__(self, report):
    if type(report) != AnalysisReport:
      return False
    # Compare Analysis values
    analysis = self.analysis == report.analysis
    data = report.data == self.data
    unalnalyzed = report.unanalyzed_repos == self.unanalyzed_repos
    vulnerabilities = report.vulnerability_data == self.vulnerability_data
    summary = report.summary == self.summary
    return analysis and data and unalnalyzed and vulnerabilities and summary

  def save_analysis_report(self, filename_addition=''):
    date_string = datetime.now().strftime('%d-%m-%y')
    filename = f'analysis_report_{date_string}{filename_addition}.pkl'
    with open(filename, 'wb') as pkl_file:
      pickle.dump(self, pkl_file, pickle.HIGHEST_PROTOCOL)
    return filename

  def get_report_data(self):
    sql = f'''
      SELECT repository_id, repo_head, completed
      FROM analysis_repo
      WHERE analysis_id = {self.analysis.id}
    '''
    q = Query()
    rows = q.query(sql)
    data_dict = {}
    for r in rows:
      sub_dict = {}
      sub_dict['repo_head'] = r[1]
      sub_dict['completed'] = r[2]
      data_dict[r[0]] = sub_dict
    return data_dict

  def summarize_data(self):
    repos_in_report = len(self.data)
    completed_repos = 0
    for id in self.data:
      datum = self.data[id]
      if datum['completed']:
        completed_repos += 1
    summary_data = {
      'repos_queried': repos_in_report,
      'repos_analyzed': completed_repos,
      'missed_repos': repos_in_report - completed_repos,
      'query': self.analysis.query,
      'codeql_version': self.analysis.codeql_version,
      'codeql_repo': self.analysis.codeql_repo
    }
    return summary_data

  def repos_analyzed(self):
    ids = []
    for id in self.data:
      datum = self.data[id]
      if datum['completed']:
        ids.append(id)
    return ids

  def vulnerabilities_found(self):
    q = Query()
    data = {}
    for repo_id in self.repos_analyzed():
      sql = f'''
        SELECT name_of_vulnerability FROM repo_vulnerabilities
        WHERE analysis_id = {self.analysis.id}
        AND repository_id = {repo_id}
      '''
      results = q.query(sql)
      # Flatten results
      vulnerabilities = [r for result in results for r in result]
      data[repo_id] = vulnerabilities
    return data
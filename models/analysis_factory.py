from db.database import Query
from models.analysis import Analysis

class AnalysisFactory:
  @staticmethod
  def find(id):
    analysis_data = AnalysisFactory.analysis_data(id)
    analysis = Analysis()
    analysis.id = id
    analysis.prepared = True
    analysis.query = analysis_data[2]
    languages = AnalysisFactory.extract_languages_from_query(analysis_data[2])
    analysis.clauses['languages'] = languages
    analysis.repo_ids = AnalysisFactory.get_repo_ids(analysis_data[2])
    return analysis

  @staticmethod
  def get_repo_ids(query):
    q = Query()
    repo_ids = q.query(query)
    # Flatten list
    ids = [r for repo_id in repo_ids for r in repo_id]
    # Remove duplicates
    ids = list(dict.fromkeys(ids))
    return ids

  @staticmethod
  def extract_languages_from_query(query):
    pgl_in = 'programming_language IN ('
    start = query.index(pgl_in) + len(pgl_in)
    split_query = query[start:]
    split_query = split_query.split(')')[0]
    languages_string = split_query.replace("'", "")
    return languages_string.split(',')

  @staticmethod
  def analysis_data(id):
    q = Query()
    analysis_row = q.get(
      'analyses',
      column='id',
      value=id
    )

    if len(analysis_row) == 0:
      raise AnalysisNotFound
    elif len(analysis_row) > 1:
      raise MultipleAnalysesFound
    else:
      analysis_row = analysis_row[0] # because Query.get returns a list of lists
    return analysis_row

class AnalysisNotFound(Exception):
  pass

class MultipleAnalysesFound(Exception):
  pass

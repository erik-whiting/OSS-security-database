from models.analysis import Analysis
languages_to_query = [
  'javascript',
  'typescript'
]

# analysis = Analysis(languages=languages_to_query)
# analysis.analyze_repositories()

# 17
analysis = Analysis(languages=languages_to_query)
analysis.id = 17
analysis.prepare()
analysis.restart_analysis()
from models.analysis import Analysis
languages_to_query = [
  'ruby',
  'javascript',
  'typescript',
  'python'
]

analysis = Analysis(languages=languages_to_query)
analysis.id = 14
analysis.prepared = True
analysis.restart_analysis()
# analysis.prepare()
# analysis.analyze_repositories()


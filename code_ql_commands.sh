# I think the initial creation of the database:
codeql database create --language=<language> --source-root <folder-to-extract> <output-folder>/<language>-database
# Tut lists this one specifically for Python
codeql database create --language=python <output-folder>/python-database

# JavaScript repositories don't require extra dependencies
# Python repositories need required versions of Python, PIP, and virtualenv

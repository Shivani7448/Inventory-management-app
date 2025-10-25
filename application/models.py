from .database import db #context of application is root directory, no dot> looks in root directory, with dot> looks in current directory
  
# 1. from database import db > models.py will look for this file in root directory
# 2. from .database import db > models.py will look for this file in current directory(application folder)
# 3. from application.database import db > models.py will think that there is one more application folder in the root directory(application folder) with respect to models.py

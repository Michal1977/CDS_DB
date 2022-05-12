from app import app, db
from app.models import CD, Band


@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "Band": Band,
       "CD": CD
   }
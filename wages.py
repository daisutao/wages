from wages import create_app
from wages.models import db, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
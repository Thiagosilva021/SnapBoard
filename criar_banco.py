from snapboard import db, app
from snapboard.models import Usuario, Postagem, Curtida

with app.app_context():
    db.create_all()

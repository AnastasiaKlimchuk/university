from core import create_app, db
import os

from models.movie import Movie

app = create_app()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=8000)

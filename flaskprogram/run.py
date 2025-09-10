from app import create_app, db
from app.models import Student, Course, Score, User

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
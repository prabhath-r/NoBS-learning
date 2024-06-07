from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    correct_answers = db.Column(db.PickleType, nullable=False)
    is_multiple_choice = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Question {self.question}>'

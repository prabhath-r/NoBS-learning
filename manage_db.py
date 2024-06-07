import os
import jsonlines
from app import db, app
from models import Question

def create_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

def check_db_content():
    with app.app_context():
        questions = Question.query.all()
        for question in questions:
            print(f'ID: {question.id}, Skill: {question.skill}, Difficulty: {question.difficulty}, Question: {question.question}')

def check_db():
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        instance_folder_exists = os.path.exists(app.instance_path)
        instance_folder_permissions = oct(os.stat(app.instance_path).st_mode)[-3:]
        db_file_exists = os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        db_file_permissions = oct(os.stat(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')).st_mode)[-3:] if db_file_exists else 'N/A'
        
        print(f"Database URI: {db_uri}")
        print(f"Instance folder exists: {instance_folder_exists}")
        print(f"Instance folder permissions: {instance_folder_permissions}")
        print(f"DB file exists: {db_file_exists}")
        print(f"DB file permissions: {db_file_permissions}")

def load_questions(filename):
    questions = []
    try:
        with jsonlines.open(filename) as reader:
            for obj in reader:
                questions.append(obj)
    except jsonlines.InvalidLineError as e:
        print(f"Error reading {filename}: {e}")
    return questions

def populate_db():
    with app.app_context():
        python_questions = load_questions('jsonl_files/python_questions.jsonl')
        ml_questions = load_questions('jsonl_files/ml_questions.jsonl')
        nn_questions = load_questions('jsonl_files/nn_questions.jsonl')

        print(f"Loaded {len(python_questions)} Python questions")
        print(f"Loaded {len(ml_questions)} Machine Learning questions")
        print(f"Loaded {len(nn_questions)} Neural Networks questions")

        for questions in [python_questions, ml_questions, nn_questions]:
            for q in questions:
                question = Question(
                    skill=q['skill'],
                    difficulty=q['difficulty'],
                    type=q['type'],
                    question=q['question'],
                    options=q['options'],
                    correct_answers=q['correct_answers'],
                    is_multiple_choice=q['is_multiple_choice']
                )
                db.session.add(question)
        db.session.commit()
        print("Database populated with questions.")

if __name__ == '__main__':
    print("Setting up database...")

    # Ensure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    os.chmod('instance', 0o755)

    # Remove existing database if it exists
    db_path = 'instance/app.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create the database
    create_db()

    # Set permissions for the app.db file
    if os.path.exists(db_path):
        os.chmod(db_path, 0o644)

    # Populate the database with questions
    populate_db()

    # Check database content
    check_db_content()

    # Check database configuration
    check_db()

import os
import jsonlines
from app import db, app
from models import Question

def create_db():
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {e}")

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
        jsonl_files_path = 'jsonl_files'
        jsonl_files = [f for f in os.listdir(jsonl_files_path) if f.endswith('.jsonl')]

        for jsonl_file in jsonl_files:
            questions = load_questions(os.path.join(jsonl_files_path, jsonl_file))
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
    print("Setting up database.....")

    os.makedirs('instance', exist_ok=True)
    os.chmod('instance', 0o755)

    db_path = 'instance/app.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    if os.path.exists(db_path):
        os.chmod(db_path, 0o644) ##gives permissions

    create_db()  ##Create the database
    populate_db()  ## Populate the database with questions

    # check_db_content() ## Check database content
    # check_db()  ## Check database configuration

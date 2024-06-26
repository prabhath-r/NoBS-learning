import os
import shutil
import json
import signal
from flask import Flask, render_template, request, jsonify, session
from models import db, Question
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Clear the sessions directory on app start
sessions_dir = os.path.join(app.instance_path, 'sessions')
if not os.path.exists(sessions_dir):
    os.makedirs(sessions_dir)

@app.route('/')
def index():
    skills = db.session.query(Question.skill).distinct().all()
    skills = [skill[0] for skill in skills]
    return render_template('index.html', skills=skills)

@app.route('/questions', methods=['GET'])
def questions():
    skill = request.args.get('skill')
    difficulty = request.args.get('difficulty')
    session['skill'] = skill
    session['difficulty'] = difficulty
    session['correct_answers'] = 0
    session['total_questions'] = 0
    session['start_time'] = datetime.now().isoformat()
    session['seen_questions'] = []
    return render_template('questions.html', skill=skill, difficulty=difficulty)

@app.route('/get_question', methods=['POST'])
def get_question():
    skill = request.form['skill']
    difficulty = request.form['difficulty'].lower()
    seen_questions = session.get('seen_questions', [])

    if difficulty == 'mastery':
        questions = Question.query.filter(Question.skill == skill, Question.id.notin_(seen_questions)).order_by(db.func.random()).all()
    else:
        questions = Question.query.filter(Question.skill == skill, Question.difficulty == difficulty, Question.id.notin_(seen_questions)).order_by(db.func.random()).all()

    if questions:
        question = questions[0]
        seen_questions.append(question.id)
        session['seen_questions'] = seen_questions
        return jsonify({
            'id': question.id,
            'question': question.question,
            'options': question.options,
            'is_multiple_choice': question.is_multiple_choice
        })
    else:
        session['seen_questions'] = []
        return jsonify({'message': 'No questions found. Resetting seen questions list. Please try again.'})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question = Question.query.get(data['id'])
    if not question:
        return jsonify({'message': 'Question not found'})

    correct = set(question.correct_answers) == set(data['answer'])
    
    # Update session data
    session['total_questions'] += 1
    if correct:
        session['correct_answers'] += 1

    return jsonify({'correct': correct, 'correct_answer': question.correct_answers})

@app.route('/end_session', methods=['POST'])
def end_session():
    end_time = datetime.now().isoformat()
    start_time = session.get('start_time')
    skill = session.get('skill')
    difficulty = session.get('difficulty')
    correct_answers = session.get('correct_answers')
    total_questions = session.get('total_questions')
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    session_data = {
        'skill': skill,
        'difficulty': difficulty,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'accuracy': accuracy,
        'start_time': start_time,
        'end_time': end_time
    }

    # Save session data to a file
    session_filename = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(os.path.join(sessions_dir, session_filename), 'w') as f:
        json.dump(session_data, f)

    return jsonify(session_data)

@app.route('/recent_sessions')
def recent_sessions():
    session_files = sorted(
        [f for f in os.listdir(sessions_dir) if f.startswith('session_')],
        key=lambda x: os.path.getmtime(os.path.join(sessions_dir, x)),
        reverse=True
    )
    recent_sessions = []
    for session_file in session_files[:10]:
        with open(os.path.join(sessions_dir, session_file), 'r') as f:
            session_data = json.load(f)
            recent_sessions.append(session_data)

    return jsonify(recent_sessions)

def clear_sessions_on_shutdown(*args):
    for filename in os.listdir(sessions_dir):
        file_path = os.path.join(sessions_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print("Session data cleared on shutdown.")

signal.signal(signal.SIGTERM, clear_sessions_on_shutdown)
signal.signal(signal.SIGINT, clear_sessions_on_shutdown)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

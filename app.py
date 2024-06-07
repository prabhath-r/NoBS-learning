from flask import Flask, render_template, request, jsonify, session
from models import db, Question
import os 
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'  # Ensure you have a secret key set
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions', methods=['GET'])
def questions():
    skill = request.args.get('skill')
    difficulty = request.args.get('difficulty')
    session['skill'] = skill
    session['difficulty'] = difficulty
    session['correct_answers'] = 0
    session['total_questions'] = 0
    session['start_time'] = datetime.now().isoformat()
    return render_template('questions.html', skill=skill, difficulty=difficulty)

@app.route('/get_question', methods=['POST'])
def get_question():
    skill = request.form['skill']
    difficulty = request.form['difficulty'].lower()

    if difficulty == 'mastery':
        questions = Question.query.filter_by(skill=skill).order_by(db.func.random()).all()
    else:
        questions = Question.query.filter_by(skill=skill, difficulty=difficulty).order_by(db.func.random()).all()

    if questions:
        question = questions[0]
        return jsonify({
            'id': question.id,
            'question': question.question,
            'options': question.options,
            'is_multiple_choice': question.is_multiple_choice
        })
    else:
        return jsonify({'message': 'No questions found'})

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
    with open(os.path.join('sessions', session_filename), 'w') as f:
        json.dump(session_data, f)

    return jsonify(session_data)

@app.route('/recent_sessions')
def recent_sessions():
    session_files = sorted(
        [f for f in os.listdir('sessions') if f.startswith('session_')],
        key=lambda x: os.path.getmtime(os.path.join('sessions', x)),
        reverse=True
    )
    recent_sessions = []
    for session_file in session_files[:10]:
        with open(os.path.join('sessions', session_file), 'r') as f:
            session_data = json.load(f)
            recent_sessions.append(session_data)

    return jsonify(recent_sessions)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

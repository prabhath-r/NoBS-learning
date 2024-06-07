# Get Started in 2 ways

## Use the App
Use the [app](https://nobs-learning.onrender.com/) to select questions from [these](https://github.com/prabhath-r/NoBS-learning/tree/main/jsonl_files) topics.  ***Note: The render server may take couple of minutes to boot up.*


## Run locally with your own questions(Best Use)

1. **Clone the Repository**

2. **Generate questions using AI Chatbots**

> *Sample Prompt:*  
> *`Generate 1000 multiple-choice questions in JSONL format below about "Generative AI" that are labelled as Easy for Hard questions, Medium for Extremely hard questions and Hard for almost Impossible questions. Ensure the questions are challenging, diverse, and help me in understanding the topic clearly. The 1000 questions could be a mix of multiple questions from each topic, covering broad range of categories. If the question/options has a part that contains code, format it to look like a code while displaying on html. The goal is to understand topics, revise those topics, advance on those topics, and improve the understanding overall. {"skill": "Skill Name", "difficulty": "easy", "type": "multiple_choice", "question": "Your question here?", "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}, "correct_answers": ["A"],"is_multiple_choice": false}`*

3. **Load the questions file to the jsonl_files folder**

4. **Run the App**: ./run.sh

5. **Access the App at http://0.0.0.0:10000 on a browser**

#### *****Tips for Best Results*****
- <span style="font-size:smaller;">*Search online and learn more on questions from unknown topics.*</span>
- <span style="font-size:smaller;">*~10,000 questions covering all the subtopics should be able to give a basic understanding or good revision on a subject.*</span>

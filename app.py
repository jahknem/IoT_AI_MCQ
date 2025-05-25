from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

# Load questions from the external JSON file
try:
    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
except FileNotFoundError:
    questions = [{"id": 0, "section": "Error", "question_text": "questions.json not found. Please create this file.", "options": [], "correct_answer_letter": "", "explanation": ""}]
except json.JSONDecodeError:
    questions = [{"id": 0, "section": "Error", "question_text": "Error decoding questions.json. Please check its format.", "options": [], "correct_answer_letter": "", "explanation": ""}]


# HTML Template for displaying questions
# Using Tailwind CSS for styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT Engineering Exam Questions</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .question-card {
            transition: all 0.3s ease-in-out;
        }
        .explanation {
            display: none; /* Hidden by default */
            background-color: #f0f9ff; /* Light blue background for explanations */
            border-left: 4px solid #3b82f6; /* Blue left border */
            border-radius: 0.375rem; /* rounded-md */
        }
        /* Base style for option labels */
        .option-label {
            border: 1px solid #e5e7eb; /* border-gray-200 */
            background-color: white;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out;
        }
        .option-label:hover {
            background-color: #f9fafb; /* hover:bg-gray-50 */
        }
        /* Correct answer style */
        .correct-answer-style {
            border-color: #10b981 !important; /* border-green-500 */
            background-color: #d1fae5 !important; /* bg-green-100 */
            color: #047857 !important; /* text-green-700 */
        }
        /* Incorrect answer style */
        .incorrect-answer-style {
            border-color: #ef4444 !important; /* border-red-500 */
            background-color: #fee2e2 !important; /* bg-red-100 */
            color: #b91c1c !important; /* text-red-700 */
        }
    </style>
</head>
<body class="bg-gray-100 text-gray-800">
    <div class="container mx-auto p-4 sm:p-8">
        <header class="mb-10 text-center">
            <h1 class="text-4xl font-bold text-gray-700">IoT Engineering Examination</h1>
            <p class="text-lg text-gray-500">Review Questions</p>
        </header>

        <div id="quizContainer">
            {% for question in questions %}
            <div class="bg-white shadow-lg rounded-lg p-6 mb-8 question-card" id="question_card_{{ question.id }}">
                <h2 class="text-xl font-semibold text-gray-700 mb-1">Question {{ question.id }}</h2>
                <p class="text-sm text-gray-500 mb-4">Section: {{ question.section }}</p>
                <p class="text-lg text-gray-800 mb-5">{{ question.question_text }}</p>
                
                <div class="space-y-3 mb-4">
                    {% for option in question.options %}
                    <label class="flex items-center p-3 rounded-md option-label" id="label_q{{ question.id }}_opt{{ option.key }}">
                        <input type="radio" 
                               name="question_{{ question.id }}" 
                               value="{{ option.key }}" 
                               class="mr-3 h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                               onchange="checkAnswer(this, '{{ question.id }}', '{{ question.correct_answer_letter }}')">
                        <span class="text-md">{{ option.key | upper }}. {{ option.text }}</span>
                    </label>
                    {% endfor %}
                </div>
                <button type="button" onclick="toggleExplanation('explanation_{{ question.id }}', this)" 
                        class="mt-2 px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                    Show Full Explanation
                </button>
                <div id="explanation_{{ question.id }}" class="explanation mt-4 p-4">
                    <p class="font-semibold">Correct Answer: {{ question.correct_answer_letter | upper }}</p>
                    <p class="text-gray-700 mt-1"><strong>Explanation:</strong> {{ question.explanation }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        function toggleExplanation(elementId, button) {
            const explanationDiv = document.getElementById(elementId);
            if (explanationDiv.style.display === 'none' || explanationDiv.style.display === '') {
                explanationDiv.style.display = 'block';
                button.textContent = 'Hide Full Explanation';
            } else {
                explanationDiv.style.display = 'none';
                button.textContent = 'Show Full Explanation';
            }
        }

        function checkAnswer(selectedRadio, questionId, correctAnswerLetter) {
            const questionCard = document.getElementById('question_card_' + questionId);
            const options = questionCard.querySelectorAll('input[type="radio"]');
            
            options.forEach(optRadio => {
                const optionKey = optRadio.value;
                const label = document.getElementById('label_q' + questionId + '_opt' + optionKey);
                
                // Reset styles
                label.classList.remove('correct-answer-style', 'incorrect-answer-style');
                // Re-add base hover if needed, or ensure base styles don't get permanently overridden
                // For simplicity, we rely on the base class 'option-label' for hover unless it's correct/incorrect

                if (optionKey === correctAnswerLetter) {
                    label.classList.add('correct-answer-style');
                }

                if (optRadio === selectedRadio && optionKey !== correctAnswerLetter) {
                    label.classList.add('incorrect-answer-style');
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def list_questions():
    """
    Renders the main page displaying all IoT questions.
    """
    return render_template_string(HTML_TEMPLATE, questions=questions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

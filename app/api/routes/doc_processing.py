import docx
import re
import os

# Function to extract questions and answers from the DOCX file
def extract_questions_and_answers(docx_path):
    if not os.path.exists(docx_path):
        print(f"The file '{docx_path}' does not exist.")
        return [], []

    doc = docx.Document(docx_path)
    
    question_pattern = r'.*\?$'  # Matches lines ending with a question mark
    
    questions = []
    answers = []
    
    current_question = None
    current_answer = []
    
    for para in doc.paragraphs:
        para_text = para.text.strip()
        
        if re.match(question_pattern, para_text):
            if current_question:
                questions.append(current_question)
                answers.append(" ".join(current_answer).strip())
            current_question = para_text
            current_answer = []
        else:
            if para_text:  # Skip empty lines
                current_answer.append(para_text)
    
    if current_question:
        questions.append(current_question)
        answers.append(" ".join(current_answer).strip())
    
    return questions, answers

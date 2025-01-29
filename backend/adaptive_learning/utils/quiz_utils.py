from django.conf import settings
from quizzes.models import Quizzes, QuizQuestions
from courses.models import Courses
import json, time, openai

openai.api_key = settings.OPENAI_API_KEY

def generate_and_save_quiz(pdf_doc):
    """
    Generate a high-quality quiz that matches the difficulty level of the provided text.
    """

    start_time = time.time() 

    prompt = f"""
    Analyze the following educational content and generate a well-structured quiz that matches its difficulty level.

    TEXT CONTENT:
    ---
    {pdf_doc.extracted_text}
    ---

    **Instructions:**
    - Identify the key concepts, important terms, and complex ideas from the text.
    - Maintain the same difficulty level as the text.
    - Generate a variety of question types: 
        1. Multiple Choice (4 options, one correct)
        2. True/False
        3. Short Answer
    - Ensure the questions test deep understanding, not just recall.
    - Provide correct answers **with explanations**.
    
    **Output format (JSON):**
    ```json
    {{
        "questions": [
            {{"type": "multiple_choice", "question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "answer": "B", "explanation": "..."}},
            {{"type": "true_false", "question": "...", "answer": true, "explanation": "..."}},
            {{"type": "short_answer", "question": "...", "answer": "...", "explanation": "..."}}
        ]
    }}
    ```

    Generate exactly 5 questions in this format.
    """

    try:
        client = openai.OpenAI() 
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI quiz generator. Return your response in strict JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,
            temperature=0.7,
            response_format={"type": "json_object"} 
        )

        response_text = completion.choices[0].message.content.strip()
        print(f"DEBUG - OpenAI Raw Response: {response_text}") 

        try:
            quiz_data = json.loads(response_text)
        except json.JSONDecodeError:
            print("ERROR - OpenAI returned invalid JSON.")
            return {"error": "OpenAI response is not valid JSON", "response_text": response_text}

        if not quiz_data.get("questions"):
            print("ERROR - OpenAI returned an empty quiz.")
            return {"error": "OpenAI response did not contain any questions", "response_text": response_text}

        quiz = Quizzes.objects.create(
            title=f"Quiz for {pdf_doc.title}",
            course=pdf_doc.course if pdf_doc.course else Courses.objects.first(),
            pdf=pdf_doc
        )

        questions_to_create = []
        for question_data in quiz_data["questions"]:
            question = QuizQuestions(
                quiz=quiz,
                question_text=question_data["question"],
                question_type=question_data["type"],
                correct_answer=question_data["answer"],
                explanation=question_data["explanation"]
            )

            if question_data["type"] == "multiple_choice":
                question.option_a = question_data["options"][0]
                question.option_b = question_data["options"][1]
                question.option_c = question_data["options"][2]
                question.option_d = question_data["options"][3]

            questions_to_create.append(question)

        QuizQuestions.objects.bulk_create(questions_to_create)  

        total_time = time.time() - start_time
        print(f"DEBUG - Total Execution Time: {total_time:.2f} seconds")

        return quiz_data 

    except openai.OpenAIError as e:
        print(f"ERROR - OpenAI API failed: {e}")
        return {"error": str(e)}

    except Exception as e:
        print(f"ERROR - Quiz generation failed: {e}")
        return {"error": str(e)}
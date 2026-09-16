from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def classify_question(question: str):
    prompt = f"""
You are a classifier for an employee policy assistant.

Classify the user's question into exactly ONE of these intents:

annual_leave
vacation
holiday
unknown

Rules:
- annual_leave: questions about annual leave, paid leave days, or how many leave days an employee receives
- vacation: questions specifically about vacation
- holiday: questions about holidays
- unknown: anything that does not belong to these categories

Return ONLY the intent name.
Do not provide an explanation.

User question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()


question = "What is my name?"

intent = classify_question(question)

print("Question:", question)
print("Intent:", intent)
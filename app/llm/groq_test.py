from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature=0
)

response = llm.invoke(
    "Explain what annual leave means in one sentence."

)

print(response.content)

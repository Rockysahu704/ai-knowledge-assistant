from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from repositories.policy_repository import get_policy
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from llm.classifier import classify_question_with_llm


load_dotenv()


llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature=0
)


class State(TypedDict):
    question: str
    intent: str
    context: str
    answer:str


def classify_question(state: State):
    print("CLASSIFY NODE")
    print("Current state:", state)
    question = state["question"]

    if "annual leave" in question.lower():
        return {"intent": "annual_leave"}

    elif "vacation" in question.lower():
        return {"intent": "vacation"}

    elif "holiday" in question.lower():
        return {"intent": "holiday"}

    else:
        intent = classify_question_with_llm(question)
        return {"intent": intent}



def retrieve_data(state: State):
    print("RETRIEVE NODE")
    print("Current state:", state)

    intent = state["intent"]

    policy = get_policy(intent)

    if policy:
        return {"context":policy}
    return {"context": "No relevant information was found."}

def generate_answer(state:State):
    #  send question + context to Groq
    question = state["question"]
    context = state["context"]

    promt = f"""
    Answer the user's question using only the provided context.

    Context:
    {context}

    Question:
    {question}

    If the context does not contain enough information to answer, 
    say that you don't have enough information.


    """
    response = llm.invoke(promt)

    return {
        "answer":response.content
    }



graph = StateGraph(State)

graph.add_node("classify_question", classify_question)
graph.add_node("retrieve_data", retrieve_data)
graph.add_node("generate_answer", generate_answer)

graph.add_edge(START, "classify_question")
graph.add_edge("classify_question", "retrieve_data")
graph.add_edge("retrieve_data", "generate_answer")
graph.add_edge("generate_answer", END)

graph = graph.compile()

result = graph.invoke({
    "question": "How many annual leave days do employees receive?"
})

print(result)
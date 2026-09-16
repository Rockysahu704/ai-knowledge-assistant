from  schemas.ask import AskQuery, AskResponse
from graph.ask_graph import graph

def ask_question(user_query: AskQuery) -> AskResponse:
    result = graph.invoke({ "question":user_query.question})

    return AskResponse(answer = result["answer"])





     
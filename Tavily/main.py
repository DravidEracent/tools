from openai import OpenAI

import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
openai_client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

def retrieve_context(question: str) -> str:
    """
    Use Tavily to fetch web context for the question.
    get_search_context gives you a ready-to-use text block for RAG.
    """
    context = tavily.get_search_context(
        query=question,
        search_depth="advanced",   # or "basic"
        max_tokens=2000,           # how much context you want back
        topic="general",           # or "news" if you're asking about news
        max_results=5,
    )
    return context


def generate_answer(question: str, context: str) -> str:
    """
    Call OpenAI with the retrieved context + question.
    """
    system_prompt = (
        "You are a helpful assistant.\n"
        "You must answer ONLY using the context given.\n"
        "If the answer is not in the context, say you don't know."
    )

    user_message = f"""Use the context below to answer the question.

    Context:
    {context}
    
    Question: {question}
    
    Answer in a few concise paragraphs:"""

    resp = openai_client.chat.completions.create(
        model="gpt-4.1-mini",  # or any other chat-capable model you have access to
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return resp.choices[0].message.content


def rag_answer(question: str) -> str:
    context = retrieve_context(question)
    answer = generate_answer(question, context)
    return answer


if __name__ == "__main__":
    q = "Summarise the latest news about Tavily search API and its use in RAG."
    print("QUESTION:\n", q)
    print("\n--- Retrieving context from web (Tavily) ---")
    ctx = retrieve_context(q)
    print(ctx[:500], "...\n")  # just show a preview

    print("--- Generating answer with RAG ---")
    ans = generate_answer(q, ctx)
    print(ans)


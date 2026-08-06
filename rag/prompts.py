from langchain_core.prompts import ChatPromptTemplate



RAG_PROMPT = ChatPromptTemplate.from_template(

"""
You are an HR assistant.

Answer only using the provided context.

If the answer is not available in the context,
say:
"I could not find this information in the HR documents."

Context:

{context}


Question:

{question}


Answer:
"""

)
from providers.llm_provider import get_llm

llm = get_llm()

response = llm.invoke("What is an HR policy?")

print(response.content)


# to run : uv run python -m tests.test_llm
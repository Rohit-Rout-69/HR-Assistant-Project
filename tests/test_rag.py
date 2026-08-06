from rag.rag_tool import search_hr_policy



result = search_hr_policy(

    "How many sick leaves are available?"

)



print(result["answer"])


print("\nSources:")


for source in result["sources"]:

    print(source)
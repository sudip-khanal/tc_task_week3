from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms.ollama import Ollama
from langchain.schema import Document
from requests.exceptions import RequestException

llm = Ollama(model="qwen2:0.5b")

def summarizer(document):
    paragraph_docs = Document(page_content=document)
    docs = [paragraph_docs]
    chain_refine = load_summarize_chain(llm, chain_type="stuff")

    try:
        result_refine = chain_refine.invoke(docs)
        return result_refine['output_text']
    except RequestException as e:
        return f"An error occurred: {str(e)}"

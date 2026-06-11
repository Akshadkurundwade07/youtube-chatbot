import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


def get_transcript(video_id: str) -> list:
    import requests

    url = "https://api.supadata.ai/v1/youtube/transcript"
    headers = {"x-api-key": "your_supadata_api_key"}
    params = {"videoId": video_id, "lang": "en"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return [{'text': c['text'], 'start': c['offset']/1000, 'duration': c['duration']/1000}
            for c in data['content']]


def build_chain(video_id: str):
    transcript_list = get_transcript(video_id)
    transcript = " ".join(chunk["text"] for chunk in transcript_list)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

    prompt = PromptTemplate(
        template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
        input_variables=['context', 'question']
    )

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain
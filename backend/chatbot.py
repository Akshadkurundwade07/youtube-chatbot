import yt_dlp
import glob
import re
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


def get_transcript(video_id: str) -> list:
    """Get transcript using YouTube Transcript API (more reliable from cloud)"""
    try:
        # Import inside function to handle version issues
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript_list = []
        for entry in transcript_data:
            transcript_list.append({
                'text': entry['text'],
                'start': entry['start'],
                'duration': entry['duration']
            })
        
        return transcript_list
    
    except Exception as e:
        # Fallback to yt-dlp if Transcript API fails
        print(f"Transcript API failed: {e}, trying yt-dlp...")
        return get_transcript_ytdlp(video_id)


def get_transcript_ytdlp(video_id: str) -> list:
    url = f"https://www.youtube.com/watch?v={video_id}"
    out_path = f"/tmp/{video_id}"

    ydl_opts = {
        'writeautomaticsub': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'skip_download': True,
        'outtmpl': out_path,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'ios'],
                'skip': ['hls', 'dash']
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    files = glob.glob(f'{out_path}*.vtt')
    if not files:
        raise ValueError("No captions found for this video. It may not have subtitles.")

    with open(files[0], 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()

    def vtt_time_to_seconds(t):
        h, m, s = t.strip().split(':')
        return round(float(h) * 3600 + float(m) * 60 + float(s), 3)

    blocks = raw.strip().split('\n\n')
    transcript_list = []
    seen_texts = set()

    for block in blocks:
        lines = block.strip().split('\n')
        time_line = next((l for l in lines if '-->' in l), None)
        if not time_line:
            continue

        times = re.findall(r'[\d:]+\.[\d]+', time_line)
        if len(times) < 2:
            continue

        start = vtt_time_to_seconds(times[0])
        end = vtt_time_to_seconds(times[1])
        duration = round(end - start, 3)

        text_lines = [l for l in lines if '-->' not in l and l.strip()
                      and not l.startswith('WEBVTT') and not l.startswith('Kind')]
        text = re.sub(r'<[^>]+>', '', ' '.join(text_lines)).strip()

        if text and text not in seen_texts:
            seen_texts.add(text)
            transcript_list.append({
                'text': text,
                'start': start,
                'duration': duration
            })

    return transcript_list


def build_chain(video_id: str):
    # Step 1: Get transcript
    transcript_list = get_transcript(video_id)
    transcript = " ".join(chunk["text"] for chunk in transcript_list)

    # Step 2: Split into chunks (exact from notebook)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    # Step 3: Embeddings + FAISS vector store (exact from notebook)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Step 4: Retriever (exact from notebook)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # Step 5: LLM (exact from notebook)
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

    # Step 6: Prompt (exact from notebook)
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

    # Step 7: Chain (exact from notebook)
    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain

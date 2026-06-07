import { useState, useRef, useEffect } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function extractVideoId(input) {
  input = input.trim();
  try {
    const url = new URL(input);
    return url.searchParams.get("v") || url.pathname.split("/").pop();
  } catch {
    return input;
  }
}

export default function App() {
  const [input, setInput] = useState("");
  const [videoId, setVideoId] = useState("");
  const [videoTitle, setVideoTitle] = useState("");
  const [status, setStatus] = useState("idle"); // idle | loading | ready | error
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [thinking, setThinking] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, thinking]);

  const loadVideo = async () => {
    const id = extractVideoId(input);
    if (!id) return;
    setStatus("loading");
    setMessages([]);
    setVideoId(id);
    setVideoTitle("");
    try {
      const res = await fetch(`${API_URL}/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id: id }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to load");
      setStatus("ready");
      setVideoTitle(`youtube.com/watch?v=${id}`);
      setMessages([
        {
          role: "bot",
          text: "Video loaded and indexed! Ask me anything about it.",
        },
      ]);
    } catch (e) {
      setStatus("error");
      setMessages([{ role: "bot", text: `❌ ${e.message}`, error: true }]);
    }
  };

  const sendMessage = async () => {
    if (!question.trim() || thinking) return;
    const q = question.trim();
    setQuestion("");
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setThinking(true);
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id: videoId, question: q }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setMessages((prev) => [...prev, { role: "bot", text: data.answer }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: `❌ ${e.message}`, error: true },
      ]);
    } finally {
      setThinking(false);
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="logo">
          <span className="logo-icon">▶</span>
          <span className="logo-text">TubeChat</span>
        </div>

        <p className="sidebar-label">YouTube URL or Video ID</p>
        <div className="url-input-wrap">
          <input
            className="url-input"
            placeholder="e.g. Gfr50f6ZBvo"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && loadVideo()}
          />
          <button
            className={`load-btn ${status === "loading" ? "loading" : ""}`}
            onClick={loadVideo}
            disabled={status === "loading" || !input.trim()}
          >
            {status === "loading" ? (
              <span className="spinner" />
            ) : (
              "Load"
            )}
          </button>
        </div>

        {videoId && (
          <div className={`status-pill ${status}`}>
            {status === "loading" && "⏳ Processing transcript…"}
            {status === "ready" && `✓ Ready — ${videoTitle}`}
            {status === "error" && "✗ Failed to load"}
          </div>
        )}

        <div className="sidebar-divider" />

        <p className="sidebar-label">Tips</p>
        <ul className="tips">
          <li>Paste a full YouTube URL or just the video ID</li>
          <li>Ask for a summary, key points, or specific details</li>
          <li>Works best with videos that have auto-captions</li>
        </ul>

        <div className="powered-by">
          Powered by <strong>Groq</strong> + <strong>LangChain</strong>
        </div>
      </div>

      <div className="main">
        <div className="chat-area">
          {messages.length === 0 && (
            <div className="empty-state">
              <div className="empty-icon">▶</div>
              <h2>Chat with any YouTube video</h2>
              <p>Paste a video URL or ID on the left to get started.</p>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`bubble-wrap ${m.role}`}>
              {m.role === "bot" && <div className="avatar bot-avatar">AI</div>}
              <div className={`bubble ${m.role} ${m.error ? "error" : ""}`}>
                {m.text}
              </div>
              {m.role === "user" && <div className="avatar user-avatar">You</div>}
            </div>
          ))}

          {thinking && (
            <div className="bubble-wrap bot">
              <div className="avatar bot-avatar">AI</div>
              <div className="bubble bot thinking">
                <span /><span /><span />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <div className="input-bar">
          <input
            className="question-input"
            placeholder={
              status === "ready"
                ? "Ask anything about the video…"
                : "Load a video first to start chatting"
            }
            value={question}
            disabled={status !== "ready"}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={status !== "ready" || !question.trim() || thinking}
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}

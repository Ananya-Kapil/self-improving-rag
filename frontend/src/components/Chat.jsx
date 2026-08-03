import { useState } from "react";
import api from "../services/api";
import SourcePanel from "./SourcePanel";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const res = await api.post("/query", {
        question: question,
        history: history,
      });

      setAnswer(res.data.answer);
      setSources(res.data.context);

      setHistory((prev) => [
        ...prev,
        {
          role: "user",
          content: question,
        },
        {
          role: "assistant",
          content: res.data.answer,
        },
      ]);

      setQuestion("");
    } catch (err) {
      console.error(err);
      setAnswer("Failed to get answer.");
      setSources([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      askQuestion();
    }
  };

  return (
    <div>
      <h2>Ask Questions</h2>

      <input
        type="text"
        placeholder="Ask about your PDF..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      <h3>Answer</h3>
      <p>{answer}</p>

      <SourcePanel sources={sources} />
    </div>
  );
}

export default Chat;
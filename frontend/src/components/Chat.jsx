import { useState } from "react";
import api from "../services/api";
import SourcePanel from "./SourcePanel";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    try {
      const res = await api.post("/query", {
        question: question,
      });

      setAnswer(res.data.answer);
      setSources(res.data.context);

    } catch (err) {
      console.error(err);
      setAnswer("Failed to get answer.");
      setSources([]);
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
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <h3>Answer</h3>
      <p>{answer}</p>

      <SourcePanel sources={sources} />
    </div>
  );
}

export default Chat;
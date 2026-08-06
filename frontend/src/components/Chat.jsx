import { useState } from "react";
import api from "../services/api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [timestamp, setTimestamp] = useState(null);

  const askQuestion = async () => {
    if (!question.trim()) return;

    try {
      const res = await api.post("/query", {
        question,
        history: [],
      });

      setAnswer(res.data.answer);

      // Save the backend-generated timestamp
      setTimestamp(res.data.timestamp);
    } catch (err) {
      console.error(err);
      setAnswer("Failed to get answer.");
    }
  };

  const sendFeedback = async (feedback) => {
    if (!timestamp) return;

    try {
      await api.post("/feedback", {
        timestamp,
        feedback,
      });

      alert("Feedback submitted successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to submit feedback.");
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

      <button onClick={askQuestion}>Ask</button>

      <h3>Answer</h3>

      <p>{answer}</p>

      {answer && (
        <div style={{ marginTop: "15px" }}>
          <button onClick={() => sendFeedback("positive")}>
            👍 Helpful
          </button>

          <button
            onClick={() => sendFeedback("negative")}
            style={{ marginLeft: "10px" }}
          >
            👎 Not Helpful
          </button>
        </div>
      )}
    </div>
  );
}

export default Chat;
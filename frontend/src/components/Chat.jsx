
import { useState } from "react";
import api from "../services/api";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [timestamp, setTimestamp] = useState(null);

  // Store previous conversation
  const [history, setHistory] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const currentQuestion = question.trim();

    try {
      const res = await api.post("/query", {
        question: currentQuestion,
        history: history,
      });

      const newAnswer = res.data.answer;

      setAnswer(newAnswer);
      setTimestamp(res.data.timestamp);

      // Add this conversation turn to history
      setHistory((prev) => [
        ...prev,
        {
          role: "user",
          content: currentQuestion,
        },
        {
          role: "assistant",
          content: newAnswer,
        },
      ]);

      // Clear input after asking
      setQuestion("");
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
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            askQuestion();
          }
        }}
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


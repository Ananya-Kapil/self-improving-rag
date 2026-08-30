
import { useEffect, useState } from "react";
import api from "../services/api";

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadAnalytics = async () => {
    try {
      setLoading(true);

      const res = await api.get("/analytics");

      setAnalytics(res.data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load analytics.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) {
    return <p>Loading analytics...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!analytics) {
    return null;
  }

  const totalQueries = analytics.total_queries || 0;
  const positive = analytics.positive || 0;
  const negative = analytics.negative || 0;

  const totalFeedback = positive + negative;

  const feedbackRate =
    totalQueries > 0
      ? (totalFeedback / totalQueries) * 100
      : 0;

  const helpfulnessRate =
    totalFeedback > 0
      ? (positive / totalFeedback) * 100
      : 0;

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>Analytics</h2>

      <div
        style={{
          display: "flex",
          gap: "30px",
          flexWrap: "wrap",
        }}
      >
        <div>
          <strong>Total Queries</strong>
          <p>{totalQueries}</p>
        </div>

        <div>
          <strong>👍 Positive</strong>
          <p>{positive}</p>
        </div>

        <div>
          <strong>👎 Negative</strong>
          <p>{negative}</p>
        </div>

        <div>
          <strong>Feedback Rate</strong>
          <p>{feedbackRate.toFixed(1)}%</p>
        </div>

        <div>
          <strong>Helpfulness Rate</strong>
          <p>{helpfulnessRate.toFixed(1)}%</p>
        </div>
      </div>

      <h3>Most Retrieved Pages</h3>

      {analytics.top_pages && analytics.top_pages.length > 0 ? (
        <ol>
          {analytics.top_pages.map(([page, count]) => (
            <li key={page}>
              Page {page} — {count} retrievals
            </li>
          ))}
        </ol>
      ) : (
        <p>No page data available yet.</p>
      )}

      <button onClick={loadAnalytics}>
        Refresh Analytics
      </button>
    </div>
  );
}

export default Analytics;


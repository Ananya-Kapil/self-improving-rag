
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

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>Analytics</h2>

      <div
        style={{
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
        }}
      >
        <div>
          <strong>Total Queries</strong>
          <p>{analytics.total_queries}</p>
        </div>

        <div>
          <strong>👍 Positive</strong>
          <p>{analytics.positive}</p>
        </div>

        <div>
          <strong>👎 Negative</strong>
          <p>{analytics.negative}</p>
        </div>

        <div>
          <strong>Feedback Rate</strong>
          <p>{analytics.feedback_rate.toFixed(1)}%</p>
        </div>

        <div>
          <strong>Helpfulness Rate</strong>
          <p>{analytics.helpfulness_rate.toFixed(1)}%</p>
        </div>

        <div>
          <strong>Feedback Chunks</strong>
          <p>{analytics.feedback_chunks}</p>
        </div>

        <div>
          <strong>Positive Chunks</strong>
          <p>{analytics.positive_chunks}</p>
        </div>

        <div>
          <strong>Negative Chunks</strong>
          <p>{analytics.negative_chunks}</p>
        </div>
      </div>

      <h3>Most Retrieved Pages</h3>

      {analytics.top_pages.length === 0 ? (
        <p>No page data available yet.</p>
      ) : (
        <ol>
          {analytics.top_pages.map(([page, count]) => (
            <li key={page}>
              Page {page} — {count} retrievals
            </li>
          ))}
        </ol>
      )}

      <button onClick={loadAnalytics}>
        Refresh Analytics
      </button>
    </div>
  );
}

export default Analytics;



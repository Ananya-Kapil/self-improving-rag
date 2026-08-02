function SourcePanel({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Retrieved Sources</h3>

      {sources.map((source, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "12px",
            marginBottom: "10px",
          }}
        >
          <p><strong>📄 File:</strong> {source.metadata.filename}</p>
          <p><strong>📃 Page:</strong> {source.metadata.page_number}</p>
          <p><strong>🔹 Chunk:</strong> {source.metadata.chunk_number}</p>

          <hr />

          <p>{source.text}</p>
        </div>
      ))}
    </div>
  );
}

export default SourcePanel;
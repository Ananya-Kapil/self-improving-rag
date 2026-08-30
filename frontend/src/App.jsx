
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import Analytics from "./components/Analytics";

function App() {
  return (
    <div style={{ padding: "40px" }}>
      <h1>Self-Improving RAG</h1>

      <Upload />

      <hr />

      <Chat />

      <hr />

      <Analytics />
    </div>
  );
}

export default App;


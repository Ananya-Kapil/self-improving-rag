import Upload from "./components/Upload";
import Chat from "./components/Chat";

function App() {
  return (
    <div style={{ padding: "40px" }}>
      <h1>Self-Improving RAG</h1>

      <Upload />

      <hr />

      <Chat />
    </div>
  );
}

export default App;
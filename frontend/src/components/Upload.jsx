import { useState } from "react";
import api from "../services/api";

function Upload() {
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setMessage("Uploading...");

      const res = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("SUCCESS:", res.data);
      setMessage(res.data.message);

    } catch (err) {
      console.error("========== ERROR ==========");

      if (err.response) {
        console.error("Status:", err.response.status);
        console.error("Data:", err.response.data);
        setMessage(`Upload failed (${err.response.status})`);
      } else if (err.request) {
        console.error("No response received:", err.request);
        setMessage("Cannot connect to backend");
      } else {
        console.error("Message:", err.message);
        setMessage(err.message);
      }

      console.error(err);
      console.error("===========================");
    }
  };

  return (
    <div>
      <h2>Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={handleUpload}
      />

      <p>{message}</p>
    </div>
  );
}

export default Upload;
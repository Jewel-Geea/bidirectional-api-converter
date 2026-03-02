import { useState } from "react";
import "./App.css";

type ConversionMode = "gql-to-rest" | "rest-to-gql";

function App() {
  const [mode, setMode] = useState<ConversionMode>("gql-to-rest");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleConvert = async () => {
    setLoading(true);
    try {
      const endpoint =
        mode === "gql-to-rest" ? "/convert/gql-to-rest" : "/convert/rest-to-gql";

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          mode === "gql-to-rest" ? { schema: input } : { openapi: input }
        ),
      });

      const data = await response.json();
      setOutput(
        mode === "gql-to-rest"
          ? JSON.stringify(data, null, 2)
          : JSON.stringify(data, null, 2)
      );
    } catch (error) {
      setOutput(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🔄 API Converter</h1>
      <p>GraphQL ↔ REST Converter with Auto-Generated Code</p>

      <div className="mode-selector">
        <button
          className={mode === "gql-to-rest" ? "active" : ""}
          onClick={() => setMode("gql-to-rest")}
        >
          GraphQL → REST
        </button>
        <button
          className={mode === "rest-to-gql" ? "active" : ""}
          onClick={() => setMode("rest-to-gql")}
        >
          REST → GraphQL
        </button>
      </div>

      <div className="editor-container">
        <div className="editor">
          <h3>Input</h3>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              mode === "gql-to-rest"
                ? "Paste your GraphQL schema here..."
                : "Paste your OpenAPI spec here..."
            }
          />
        </div>

        <div className="editor">
          <h3>Output</h3>
          <textarea value={output} readOnly placeholder="Converted output will appear here..." />
        </div>
      </div>

      <button className="convert-btn" onClick={handleConvert} disabled={loading || !input}>
        {loading ? "Converting..." : "Convert"}
      </button>
    </div>
  );
}

export default App;

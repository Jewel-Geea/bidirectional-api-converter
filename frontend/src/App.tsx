import { useState } from "react";
import "./App.css";

type ConversionMode = "gql-to-rest" | "rest-to-gql";
type Tab = "spec" | "code";

function App() {
  const [mode, setMode] = useState<ConversionMode>("gql-to-rest");
  const [input, setInput] = useState("");
  const [spec, setSpec] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<Tab>("spec");
  const [error, setError] = useState("");

  const handleConvert = async () => {
    setLoading(true);
    setError("");
    try {
      const endpoint = mode === "gql-to-rest" ? "/convert/gql-to-rest" : "/convert/rest-to-gql";
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mode === "gql-to-rest" ? { schema: input } : { openapi: input }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Conversion failed");
      }

      const data = await response.json();
      setSpec(JSON.stringify(data.spec, null, 2));
      setCode(data.code);
    } catch (err: any) {
      setError(err.message);
      setSpec("");
      setCode("");
    } finally {
      setLoading(false);
    }
  };

  const handleModeChange = (newMode: ConversionMode) => {
    setMode(newMode);
    setInput("");
    setSpec("");
    setCode("");
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <path
              d="M16 4L28 10V22L16 28L4 22V10L16 4Z"
              stroke="#58a6ff"
              strokeWidth="2"
              fill="none"
            />
            <circle cx="16" cy="16" r="4" fill="#58a6ff" />
          </svg>
          <h1>API Converter</h1>
        </div>
        <p>Transform APIs instantly • GraphQL ↔ REST</p>
      </header>

      <div className="mode-selector">
        <button
          className={mode === "gql-to-rest" ? "active" : ""}
          onClick={() => handleModeChange("gql-to-rest")}
        >
          <span className="icon">⚡</span>
          GraphQL → REST
        </button>
        <button
          className={mode === "rest-to-gql" ? "active" : ""}
          onClick={() => handleModeChange("rest-to-gql")}
        >
          <span className="icon">🔄</span>
          REST → GraphQL
        </button>
      </div>

      <div className="workspace">
        <div className="panel input-panel">
          <div className="panel-header">
            <h3>Input</h3>
            <span className="badge">{mode === "gql-to-rest" ? "GraphQL SDL" : "OpenAPI JSON"}</span>
          </div>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              mode === "gql-to-rest"
                ? "type User {\n  id: ID!\n  name: String!\n}\n\ntype Query {\n  user(id: ID!): User\n}"
                : '{\n  "openapi": "3.0.0",\n  "paths": {\n    "/users": {\n      "get": {}\n    }\n  }\n}'
            }
            spellCheck={false}
          />
        </div>

        <div className="panel output-panel">
          <div className="panel-header">
            <h3>Output</h3>
            <div className="tabs">
              <button
                className={activeTab === "spec" ? "active" : ""}
                onClick={() => setActiveTab("spec")}
              >
                Specification
              </button>
              <button
                className={activeTab === "code" ? "active" : ""}
                onClick={() => setActiveTab("code")}
              >
                Generated Code
              </button>
            </div>
          </div>
          {error ? (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          ) : (
            <textarea
              value={activeTab === "spec" ? spec : code}
              readOnly
              placeholder={loading ? "Converting..." : "Output will appear here..."}
              spellCheck={false}
            />
          )}
        </div>
      </div>

      <button className="convert-btn" onClick={handleConvert} disabled={loading || !input}>
        {loading ? (
          <>
            <span className="spinner"></span>
            Converting...
          </>
        ) : (
          <>
            <span className="icon">✨</span>
            Convert
          </>
        )}
      </button>
    </div>
  );
}

export default App;

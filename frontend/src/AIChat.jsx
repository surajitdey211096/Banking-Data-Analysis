
import React, { useState } from "react";
import {
  Bot,
  Send,
  User,
  LoaderCircle,
  AlertCircle,
} from "lucide-react";

// Backend API configuration
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export default function AIChat() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! Ask me about banking analytics, transactions, loans, or fraud alerts.",
      sources: [],
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Submit question to the backend
  async function handleSubmit(event) {
    event.preventDefault();

    const userQuestion = question.trim();

    if (!userQuestion || loading) {
      return;
    }

    // Display the user question
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setError("");
    setLoading(true);

    try {
      // Call the RAG API endpoint
      const response = await fetch(
        `${API_BASE_URL}/api/rag/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      // Read the JSON response
      const result = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          result.detail ||
            result.message ||
            `Request failed with status ${response.status}`
        );
      }

      // Display the AI response
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            result.answer ||
            result.response ||
            "The API returned no answer.",
          sources: Array.isArray(result.sources)
            ? result.sources
            : [],
        },
      ]);
    } catch (err) {
      console.error("Banking RAG API error:", err);

      setError(
        err.message ||
          "Unable to connect to the banking analytics API."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="ai-chat">
      {/* Chat header */}
      <header className="ai-chat__header">
        <span className="ai-chat__avatar">
          <Bot size={22} />
        </span>

        <div>
          <h3>Banking AI Assistant</h3>
          <p>Powered by your RAG backend</p>
        </div>
      </header>

      {/* Chat messages */}
      <div
        className="ai-chat__messages"
        aria-live="polite"
        aria-busy={loading}
      >
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`ai-chat__message ${message.role}`}
          >
            <span className="ai-chat__message-icon">
              {message.role === "user" ? (
                <User size={17} />
              ) : (
                <Bot size={17} />
              )}
            </span>

            <div className="ai-chat__bubble">
              <p>{message.content}</p>

              {/* Retrieved RAG sources */}
              {message.sources?.length > 0 && (
                <details className="ai-chat__sources">
                  <summary>
                    Sources ({message.sources.length})
                  </summary>

                  <ul>
                    {message.sources.map(
                      (source, sourceIndex) => (
                        <li
                          key={`${source.id ?? sourceIndex}-${sourceIndex}`}
                        >
                          Record: {source.id ?? "Unknown"}
                          {source.score != null &&
                            ` · Similarity: ${source.score}`}
                        </li>
                      )
                    )}
                  </ul>
                </details>
              )}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="ai-chat__loading">
            <LoaderCircle size={18} className="spin" />
            Searching banking records...
          </div>
        )}

        {/* Error message */}
        {error && (
          <p className="ai-chat__error" role="alert">
            <AlertCircle size={16} />
            {" "}{error}
          </p>
        )}
      </div>

      {/* Question input */}
      <form
        className="ai-chat__form"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask about transactions or loans..."
          aria-label="Ask the banking AI assistant"
          disabled={loading}
          maxLength={1000}
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
          aria-label="Send question"
        >
          {loading ? (
            <LoaderCircle size={18} className="spin" />
          ) : (
            <Send size={18} />
          )}
        </button>
      </form>

      {/* Disclaimer */}
      <p className="ai-chat__disclaimer">
        Verify financial results against your validated source data.
        Do not enter confidential customer information.
      </p>
    </section>
  );
}

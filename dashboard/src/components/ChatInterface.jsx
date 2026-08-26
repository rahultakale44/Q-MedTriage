/**
 * RESULT-SPECIFIC CHAT INTERFACE
 */

import { useState, useRef, useEffect } from "react";
import { Send, Sparkles, User, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { askQuestion } from "../services/api";

const QUICK_QUESTIONS = [
  "Why this prediction?",
  "Show evidence",
  "Explain simply",
  "What does confidence mean?",
];

export function ChatInterface({ predictionData, image, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "I can help you understand this analysis. Ask me anything about the prediction, evidence, or results.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async (question = input) => {
    if (!question.trim() || isLoading) return;

    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await askQuestion(question, {
        prediction: predictionData,
        image: image,
      });

      if (response.success) {
        const assistantMessage = {
          role: "assistant",
          content: response.data.answer || response.data.explanation || "I apologize, but I couldn't generate a response.",
          sources: response.data.sources,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      const errorMessage = {
        role: "assistant",
        content: `I encountered an error: ${error.message}. Please try again.`,
        error: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    handleSend(question);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const prediction = predictionData?.triage?.prediction || "UNKNOWN";
  const confidence = predictionData?.triage?.confidence || 0;

  return (
    <motion.div
      className="chat-interface"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="chat-container">
        <div className="chat-header">
          <div className="chat-title-group">
            <Sparkles size={24} />
            <div>
              <h2>Q-MedTriage Intelligence</h2>
              <p className="chat-subtitle">Analysis Session</p>
            </div>
          </div>
          <button className="chat-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="chat-result-summary">
          <div className="summary-label">CURRENT RESULT</div>
          <div className="summary-prediction">
            {prediction} · {(confidence * 100).toFixed(1)}%
          </div>
        </div>

        <div className="chat-messages">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                className={`chat-message ${message.role}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="message-avatar">
                  {message.role === "user" ? <User size={18} /> : <Sparkles size={18} />}
                </div>
                <div className="message-content">
                  <div className="message-role">
                    {message.role === "user" ? "YOU" : "Q-MEDTRIAGE"}
                  </div>
                  <div className="message-text">{message.content}</div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <div className="sources-label">Sources:</div>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className="source-item">
                          • {source.title}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              className="chat-message assistant loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="message-avatar">
                <Sparkles size={18} />
              </div>
              <div className="message-content">
                <div className="message-role">Q-MEDTRIAGE</div>
                <div className="message-text">
                  <motion.span
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    Thinking...
                  </motion.span>
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {messages.length === 1 && (
          <div className="chat-quick-questions">
            {QUICK_QUESTIONS.map((question, index) => (
              <motion.button
                key={index}
                className="quick-question-chip"
                onClick={() => handleQuickQuestion(question)}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {question}
              </motion.button>
            ))}
          </div>
        )}

        <div className="chat-input-container">
          <input
            ref={inputRef}
            type="text"
            className="chat-input"
            placeholder="Ask about this result..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            className="chat-send-button"
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </motion.div>
  );
}

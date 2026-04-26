import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, ThumbsUp, ThumbsDown, Loader } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useChatStore } from '../store/store';
import { chatAPI } from '../api/apiClient';

const normalizeMessageContent = (content) => {
  if (typeof content === 'string') return content;
  if (content == null) return '';
  return String(content);
};

const normalizeConditions = (conditions) => {
  if (!Array.isArray(conditions)) return [];

  return conditions.filter((cond) => (
    Array.isArray(cond) &&
    cond.length >= 2 &&
    typeof cond[0] === 'string' &&
    Number.isFinite(Number(cond[1]))
  ));
};

const ChatTab = () => {
  const { messages, addMessage, isLoading, setLoading, userId, clearMessages } = useChatStore();
  const [input, setInput] = useState('');
  const [feedback, setFeedback] = useState({});
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');

    addMessage({
      id: Date.now(),
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    });

    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(userMessage, userId);

      addMessage({
        id: response.message_id,
        role: 'assistant',
        content: response.response,
        healthcare_mode: response.healthcare_mode,
        symptoms: response.detected_symptoms,
        conditions: response.conditions,
        timestamp: new Date(),
      });

      setFeedback((prev) => ({
        ...prev,
        [response.message_id]: null
      }));
    } catch (error) {
      addMessage({
        id: Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (messageId, isHelpful) => {
    try {
      await chatAPI.submitFeedback(messageId, isHelpful, 'general');
      setFeedback((prev) => ({
        ...prev,
        [messageId]: isHelpful
      }));
    } catch (error) {
      console.error('Feedback error:', error);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-300px)] rounded-2xl overflow-hidden glass border dark:border-slate-700">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-full flex flex-col items-center justify-center text-center"
          >
            <div className="text-6xl mb-4">
              Hospital
            </div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
              Welcome to Your Health Assistant
            </h2>
            <p className="text-slate-600 dark:text-slate-400 max-w-md">
              I&apos;m here to help you understand your health better. Ask me about your symptoms, health concerns, or general wellness questions.
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-500 mt-4">
              Remember: I provide information, not medical diagnosis.
            </p>
          </motion.div>
        ) : (
          <AnimatePresence>
            {messages.map((message) => {
              const safeContent = normalizeMessageContent(message.content);
              const safeConditions = normalizeConditions(message.conditions);

              return (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -100 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-md lg:max-w-xl rounded-2xl px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-cyan-600 to-cyan-500 text-white rounded-br-none'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white rounded-bl-none'
                    }`}
                  >
                    {message.role === 'assistant' ? (
                      <div className="text-sm leading-relaxed">
                        <ReactMarkdown
                          components={{
                            h1: (props) => <h1 className="text-base font-semibold mt-3 mb-2" {...props} />,
                            h2: (props) => <h2 className="text-base font-semibold mt-3 mb-2" {...props} />,
                            h3: (props) => <h3 className="text-sm font-semibold mt-3 mb-2" {...props} />,
                            p: (props) => <p className="my-1" {...props} />,
                            ul: (props) => <ul className="my-2 pl-5 list-disc space-y-1" {...props} />,
                            ol: (props) => <ol className="my-2 pl-5 list-decimal space-y-1" {...props} />,
                            li: (props) => <li className="my-0.5" {...props} />,
                          }}
                        >
                          {safeContent}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <p className="text-sm leading-relaxed">{safeContent}</p>
                    )}

                    {message.healthcare_mode && (
                      <div className="mt-3 pt-3 border-t border-slate-300 dark:border-slate-600 text-xs space-y-2">
                        {Array.isArray(message.symptoms) && message.symptoms.length > 0 && (
                          <div>
                            <p className="font-semibold opacity-80">Detected Symptoms:</p>
                            <p className="opacity-70">{message.symptoms.join(', ')}</p>
                          </div>
                        )}
                        {safeConditions.length > 0 && (
                          <div>
                            <p className="font-semibold opacity-80">Possible Conditions:</p>
                            <div className="space-y-1 opacity-70">
                              {safeConditions.map((cond, i) => (
                                <p key={`${message.id}-condition-${i}`}>- {cond[0]} ({Math.round(Number(cond[1]) * 100)}%)</p>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {message.role === 'assistant' && (
                      <div className="flex space-x-2 mt-3">
                        <button
                          onClick={() => handleFeedback(message.id, true)}
                          className={`p-1 rounded transition ${
                            feedback[message.id] === true
                              ? 'bg-emerald-500 text-white'
                              : 'hover:bg-slate-200 dark:hover:bg-slate-700'
                          }`}
                          title="Helpful"
                        >
                          <ThumbsUp size={16} />
                        </button>
                        <button
                          onClick={() => handleFeedback(message.id, false)}
                          className={`p-1 rounded transition ${
                            feedback[message.id] === false
                              ? 'bg-red-500 text-white'
                              : 'hover:bg-slate-200 dark:hover:bg-slate-700'
                          }`}
                          title="Not helpful"
                        >
                          <ThumbsDown size={16} />
                        </button>
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        )}

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex space-x-2"
          >
            <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-4 py-3">
              <motion.div
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="flex space-x-2"
              >
                <div className="w-2 h-2 bg-slate-400 rounded-full" />
                <div className="w-2 h-2 bg-slate-400 rounded-full" />
                <div className="w-2 h-2 bg-slate-400 rounded-full" />
              </motion.div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t dark:border-slate-700 p-4 bg-slate-50/50 dark:bg-slate-900/50">
        <form onSubmit={handleSendMessage} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tell me about your symptoms or ask a health question..."
            disabled={isLoading}
            className="flex-1 px-4 py-3 rounded-xl bg-white dark:bg-slate-800 border dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-cyan-500 disabled:opacity-50"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-3 rounded-xl bg-gradient-to-r from-cyan-600 to-cyan-500 text-white hover:shadow-lg disabled:opacity-50 transition flex items-center space-x-2"
          >
            {isLoading ? <Loader size={20} className="animate-spin" /> : <Send size={20} />}
          </motion.button>
        </form>

        {messages.length > 0 && (
          <button
            onClick={clearMessages}
            className="mt-2 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition"
          >
            Clear chat history
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatTab;

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, MessageSquare, Shield, Settings } from 'lucide-react';
import { useChatStore } from './store/store';
import { chatAPI } from './api/apiClient';

import ChatTab from './pages/ChatTab';
import InsightsTab from './pages/InsightsTab';
import SecurityTab from './pages/SecurityTab';
import SettingsTab from './pages/SettingsTab';

import './index.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [isConnected, setIsConnected] = useState(false);
  const { darkMode, toggleDarkMode } = useChatStore();

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  useEffect(() => {
    // Check API connection
    chatAPI.healthCheck()
      .then(() => setIsConnected(true))
      .catch(() => setIsConnected(false));
  }, []);

  const tabs = [
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'insights', label: 'Health Insights', icon: Brain },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-950 dark:to-slate-900 min-h-screen">
        
        {/* Header */}
        <header className="sticky top-0 z-40 glass border-b dark:border-slate-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                  className="text-3xl"
                >
                  🏥
                </motion.div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-emerald-600 bg-clip-text text-transparent">
                    AI Healthcare
                  </h1>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Secure AI-Powered Health Assistant
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                {/* Status Indicator */}
                <div className="flex items-center space-x-2">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className={`w-3 h-3 rounded-full ${
                      isConnected ? 'bg-emerald-500' : 'bg-red-500'
                    }`}
                  />
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    {isConnected ? 'Connected' : 'Offline'}
                  </span>
                </div>

                {/* Dark Mode Toggle */}
                <button
                  onClick={toggleDarkMode}
                  className="p-2 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition"
                >
                  {darkMode ? '☀️' : '🌙'}
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Tab Navigation */}
        <div className="sticky top-20 z-30 glass border-b dark:border-slate-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-1 overflow-x-auto">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                
                return (
                  <motion.button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-3 font-medium text-sm flex items-center space-x-2 border-b-2 transition ${
                      isActive
                        ? 'border-cyan-600 text-cyan-600 dark:text-cyan-400'
                        : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-300'
                    }`}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Icon size={18} />
                    <span>{tab.label}</span>
                  </motion.button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Tab Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'chat' && <ChatTab />}
              {activeTab === 'insights' && <InsightsTab />}
              {activeTab === 'security' && <SecurityTab />}
              {activeTab === 'settings' && <SettingsTab />}
            </motion.div>
          </AnimatePresence>
        </main>

        {/* Footer */}
        <footer className="border-t dark:border-slate-700 glass mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-slate-600 dark:text-slate-400">
            <p>
              ⚠️ <strong>Medical Disclaimer:</strong> This is an AI assistant, not a doctor. 
              Always consult healthcare professionals for medical advice.
            </p>
            <p className="mt-2">v1.0.0 © 2024 AI Healthcare Platform</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default App;

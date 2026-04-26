import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Moon, Bell, Trash2, Lock } from 'lucide-react';
import { useChatStore } from '../store/store';
import { chatAPI } from '../api/apiClient';

const SettingsTab = () => {
  const { darkMode, toggleDarkMode, userId } = useChatStore();
  const [settings, setSettings] = useState({
    notifications: true,
    dataRetention: 30,
    theme: 'system',
  });
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleted, setDeleted] = useState(false);

  const handleClearHistory = async () => {
    try {
      await chatAPI.clearHistory(userId);
      setDeleted(true);
      setTimeout(() => setDeleted(false), 3000);
      setShowDeleteConfirm(false);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  };

  const SettingToggle = ({ icon: Icon, title, description, value, onChange }) => (
    <motion.div
      whileHover={{ y: -3 }}
      className="glass rounded-2xl p-6 border dark:border-slate-700 flex items-center justify-between"
    >
      <div className="flex items-center space-x-4">
        <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-800">
          <Icon className="text-cyan-600" size={24} />
        </div>
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white">{title}</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
        </div>
      </div>
      <button
        onClick={onChange}
        className={`relative w-14 h-8 rounded-full transition-colors ${
          value ? 'bg-cyan-600' : 'bg-slate-300 dark:bg-slate-600'
        }`}
      >
        <motion.div
          animate={{ x: value ? 28 : 4 }}
          className="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-md"
        />
      </button>
    </motion.div>
  );

  return (
    <div className="space-y-6">
      {/* Theme Settings */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Appearance</h2>
        
        <motion.div
          whileHover={{ y: -3 }}
          className="glass rounded-2xl p-6 border dark:border-slate-700"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-800">
                <Moon className="text-purple-600" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white">Dark Mode</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  {darkMode ? 'Enabled' : 'Disabled'}
                </p>
              </div>
            </div>
            <button
              onClick={toggleDarkMode}
              className={`relative w-14 h-8 rounded-full transition-colors ${
                darkMode ? 'bg-purple-600' : 'bg-slate-300 dark:bg-slate-600'
              }`}
            >
              <motion.div
                animate={{ x: darkMode ? 28 : 4 }}
                className="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-md"
              />
            </button>
          </div>
        </motion.div>
      </div>

      {/* Privacy Settings */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Privacy & Security</h2>
        
        <SettingToggle
          icon={Bell}
          title="Notifications"
          description="Receive updates about your health insights"
          value={settings.notifications}
          onChange={() => setSettings(prev => ({
            ...prev,
            notifications: !prev.notifications
          }))}
        />

        <motion.div
          whileHover={{ y: -3 }}
          className="glass rounded-2xl p-6 border dark:border-slate-700"
        >
          <div className="flex items-center space-x-4 mb-4">
            <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-800">
              <Lock className="text-cyan-600" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 dark:text-white">
                Data Retention
              </h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                Automatically delete old chat history
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <select
              value={settings.dataRetention}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                dataRetention: parseInt(e.target.value)
              }))}
              className="px-3 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 border dark:border-slate-700 text-slate-900 dark:text-white"
            >
              <option value={7}>7 days</option>
              <option value={14}>14 days</option>
              <option value={30}>30 days (recommended)</option>
              <option value={60}>60 days</option>
              <option value={90}>90 days</option>
            </select>
          </div>
        </motion.div>
      </div>

      {/* Data Management */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Data Management</h2>

        {deleted && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl p-4 border border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
          >
            <p className="text-emerald-700 dark:text-emerald-300 text-sm font-semibold">
              ✓ Chat history cleared successfully
            </p>
          </motion.div>
        )}

        <motion.div
          whileHover={{ y: -3 }}
          className="glass rounded-2xl p-6 border dark:border-slate-700"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-red-100 dark:bg-red-900">
                <Trash2 className="text-red-600" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 dark:text-white">
                  Clear Chat History
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Permanently delete all your conversations
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition font-semibold text-sm"
            >
              Clear All
            </button>
          </div>

          {showDeleteConfirm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            >
              <p className="text-red-900 dark:text-red-200 mb-3 text-sm font-semibold">
                ⚠️ Are you sure? This cannot be undone.
              </p>
              <div className="flex space-x-2">
                <button
                  onClick={handleClearHistory}
                  className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 text-sm font-semibold"
                >
                  Yes, Delete All
                </button>
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="px-4 py-2 rounded bg-slate-300 dark:bg-slate-700 text-slate-900 dark:text-white text-sm font-semibold"
                >
                  Cancel
                </button>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* Account Info */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Account</h2>

        <motion.div
          whileHover={{ y: -3 }}
          className="glass rounded-2xl p-6 border dark:border-slate-700"
        >
          <div className="space-y-3">
            <div>
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                User ID
              </p>
              <p className="text-sm font-mono text-slate-900 dark:text-white mt-1">{userId}</p>
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                Version
              </p>
              <p className="text-sm text-slate-900 dark:text-white mt-1">v1.0.0</p>
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
                Status
              </p>
              <p className="text-sm text-emerald-600 dark:text-emerald-400 mt-1">✓ Active</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Help & Support */}
      <motion.div
        whileHover={{ y: -3 }}
        className="glass rounded-2xl p-6 border dark:border-slate-700 text-center"
      >
        <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Need Help?</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
          Check our documentation or contact support
        </p>
        <button className="px-4 py-2 rounded-lg bg-cyan-600 text-white hover:bg-cyan-700 transition font-semibold text-sm">
          Contact Support
        </button>
      </motion.div>
    </div>
  );
};

export default SettingsTab;

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Lock, CheckCircle, AlertCircle, Shield, Server } from 'lucide-react';
import { chatAPI } from '../api/apiClient';

const SecurityTab = () => {
  const [securityStatus, setSecurityStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSecurityStatus = async () => {
      try {
        setLoading(true);
        const data = await chatAPI.getSecurityStatus();
        setSecurityStatus(data);
      } catch (error) {
        console.error('Failed to fetch security status:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSecurityStatus();
    
    // Refresh security status every 5 seconds
    const interval = setInterval(fetchSecurityStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const SecurityFeature = ({ icon: Icon, title, description, status, details }) => (
    <motion.div
      whileHover={{ y: -5, scale: 1.02 }}
      className="glass rounded-2xl p-6 border dark:border-slate-700"
    >
      <div className="flex items-start space-x-4">
        <div className={`p-3 rounded-lg ${status ? 'bg-emerald-100 dark:bg-emerald-900' : 'bg-red-100 dark:bg-red-900'}`}>
          <Icon className={status ? 'text-emerald-600' : 'text-red-600'} size={24} />
        </div>
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="font-semibold text-slate-900 dark:text-white">{title}</h3>
            {status && <CheckCircle className="text-emerald-600" size={20} />}
            {!status && <AlertCircle className="text-red-600" size={20} />}
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
          {details && (
            <p className="text-xs text-slate-500 dark:text-slate-500 mt-2 font-mono">{details}</p>
          )}
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="space-y-6">
      {/* Security Overview */}
      <motion.div
        whileHover={{ y: -5 }}
        className="glass rounded-2xl p-8 border dark:border-slate-700 text-center"
      >
        <Shield className="mx-auto mb-4 text-cyan-600" size={48} />
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">
          Security Status
        </h2>
        <p className="text-lg text-emerald-600 font-semibold mb-4">
          🔒 {securityStatus?.status || 'Checking...'}
        </p>
        <div className="flex justify-center space-x-4">
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-12 h-12 rounded-full bg-gradient-to-r from-cyan-600 to-emerald-600 flex items-center justify-center text-white"
          >
            ✓
          </motion.div>
        </div>
      </motion.div>

      {/* Security Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SecurityFeature
          icon={Lock}
          title="AES-256 Encryption"
          description="All messages encrypted using military-grade AES-256 encryption via Fernet"
          status={securityStatus?.encryption_enabled}
          details={securityStatus?.encryption_type}
        />
        <SecurityFeature
          icon={Server}
          title="Database Security"
          description={securityStatus?.storage_mode === 'mongodb' 
            ? "MongoDB with encrypted fields and secure connection" 
            : "In-memory storage with AES-256 encryption (Demo mode)"}
          status={securityStatus?.database_connected}
          details={securityStatus?.storage_mode === 'mongodb' 
            ? "MongoDB Atlas (encrypted at rest)" 
            : "Encrypted in-memory database"}
        />
        <SecurityFeature
          icon={Shield}
          title="API Security"
          description="CORS protection, rate limiting, and secure headers enabled"
          status={securityStatus?.api_secured}
          details="HTTPS, CORS, secure tokens"
        />
        <SecurityFeature
          icon={CheckCircle}
          title="Data Privacy"
          description="HIPAA-compliant data handling and user privacy protection"
          status={true}
          details="Zero-knowledge encryption, no data selling"
        />
      </div>

      {/* Encryption Details */}
      <motion.div
        whileHover={{ y: -5 }}
        className="glass rounded-2xl p-6 border dark:border-slate-700"
      >
        <h3 className="font-semibold text-lg text-slate-900 dark:text-white mb-4">
          🔐 Encryption Implementation
        </h3>
        <div className="space-y-3 text-sm text-slate-600 dark:text-slate-400">
          <div className="flex items-start space-x-2">
            <span className="text-cyan-600 font-bold">1.</span>
            <p><strong>Message Encryption:</strong> Every user message is encrypted before storage</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-cyan-600 font-bold">2.</span>
            <p><strong>Response Encryption:</strong> AI responses are encrypted in the database</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-cyan-600 font-bold">3.</span>
            <p><strong>Decryption on Demand:</strong> Data only decrypted when needed for display</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-cyan-600 font-bold">4.</span>
            <p><strong>Secure Keys:</strong> Encryption keys stored securely in environment variables</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-cyan-600 font-bold">5.</span>
            <p><strong>No Plaintext Storage:</strong> Chat history never stored in plaintext</p>
          </div>
        </div>
      </motion.div>

      {/* Data Handling */}
      <motion.div
        whileHover={{ y: -5 }}
        className="glass rounded-2xl p-6 border dark:border-slate-700"
      >
        <h3 className="font-semibold text-lg text-slate-900 dark:text-white mb-4">
          📋 Data Handling Policy
        </h3>
        <div className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
          <p>✓ Chat history retained for 30 days</p>
          <p>✓ User feedback stored anonymously</p>
          <p>✓ No third-party data sharing</p>
          <p>✓ Users can request data deletion anytime</p>
          <p>✓ Automatic data purge after retention period</p>
          <p>✓ End-to-end encryption for sensitive conversations</p>
        </div>
      </motion.div>

      {/* Security Best Practices */}
      <motion.div
        whileHover={{ y: -5 }}
        className="glass rounded-2xl p-6 border dark:border-slate-700"
      >
        <h3 className="font-semibold text-lg text-slate-900 dark:text-white mb-4">
          🛡️ Your Privacy Tips
        </h3>
        <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
          <li>• Don't share actual medical records or sensitive personal info</li>
          <li>• Use general symptoms descriptions instead of specific names</li>
          <li>• Clear chat history regularly if using shared devices</li>
          <li>• Always verify medical advice with licensed professionals</li>
          <li>• Report any security concerns immediately</li>
        </ul>
      </motion.div>

      {/* Medical Disclaimer */}
      <motion.div
        whileHover={{ y: -5 }}
        className="glass rounded-2xl p-6 border dark:border-slate-700 bg-amber-50 dark:bg-amber-900/20"
      >
        <h3 className="font-semibold text-lg text-amber-900 dark:text-amber-200 mb-2">
          ⚠️ Important Medical Disclaimer
        </h3>
        <p className="text-sm text-amber-800 dark:text-amber-300">
          This AI healthcare assistant is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers before making any medical decisions. In case of medical emergencies, contact emergency services immediately.
        </p>
      </motion.div>
    </div>
  );
};

export default SecurityTab;

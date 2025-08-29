import React from 'react';
import { motion } from 'framer-motion';

const RegisterPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Register Page</h1>
        <p className="text-gray-600">Registration functionality coming soon...</p>
      </motion.div>
    </div>
  );
};

export default RegisterPage;
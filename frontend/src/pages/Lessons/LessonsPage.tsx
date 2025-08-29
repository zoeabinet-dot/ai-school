import React from 'react';
import { motion } from 'framer-motion';

const LessonsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-sm p-6"
      >
        <h1 className="text-2xl font-bold text-gray-900 mb-4">LessonsPage</h1>
        <p className="text-gray-600">LessonsPage functionality coming soon...</p>
      </motion.div>
    </div>
  );
};

export default LessonsPage;

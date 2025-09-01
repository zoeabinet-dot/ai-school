import React from 'react';
import { useParams } from 'react-router-dom';

const StudentDetailPage: React.FC = () => {
  const { id } = useParams();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Student Detail</h1>
      <p className="mt-4">Student ID: {id}</p>
      <p className="mt-2 text-sm text-gray-600">This is a placeholder student detail page.</p>
    </div>
  );
};

export default StudentDetailPage;

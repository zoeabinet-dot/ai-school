import React from 'react';
import { useParams } from 'react-router-dom';

const AILessonDetailPage: React.FC = () => {
  const { id } = useParams();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">AI Lesson Detail</h1>
      <p className="mt-4">Lesson ID: {id}</p>
      <p className="mt-2 text-sm text-gray-600">This is a placeholder AI lesson detail page.</p>
    </div>
  );
};

export default AILessonDetailPage;

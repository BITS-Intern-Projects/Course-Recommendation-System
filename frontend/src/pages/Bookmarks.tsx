import { useState, useEffect } from 'react';
import axios from 'axios';

interface Course {
  id: string;
  name: string;
  description: string;
  url: string;
}

function Bookmarks() {
  const [bookmarks, setBookmarks] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    try {
      const response = await axios.get('http://localhost:8000/bookmarks');
      setBookmarks(response.data);
    } catch (error) {
      console.error('Error fetching bookmarks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveBookmark = async (courseId: string) => {
    try {
      await axios.delete(`http://localhost:8000/bookmark/${courseId}`);
      setBookmarks(bookmarks.filter(bookmark => bookmark.id !== courseId));
    } catch (error) {
      console.error('Error removing bookmark:', error);
    }
  };

  const handleCourseClick = async (course: Course) => {
    try {
      await axios.post('http://localhost:8000/track-click', { courseId: course.id });
      window.open(course.url, '_blank');
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  if (loading) {
    return <div className="text-center">Loading bookmarks...</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Your Bookmarked Courses</h2>
      {bookmarks.length === 0 ? (
        <p className="text-gray-600">No bookmarked courses yet.</p>
      ) : (
        <div className="space-y-4">
          {bookmarks.map((course) => (
            <div key={course.id} className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900">{course.name}</h3>
              <p className="mt-2 text-gray-600">{course.description}</p>
              <div className="mt-4 flex space-x-4">
                <button
                  onClick={() => handleCourseClick(course)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  View Course
                </button>
                <button
                  onClick={() => handleRemoveBookmark(course.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Remove Bookmark
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Bookmarks; 
import { useState } from 'react';
import axios from 'axios';

interface Course {
  id: string;
  name: string;
  description: string;
  url: string;
}

function Home() {
  const [query, setQuery] = useState('');
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Submit query
      await axios.post('http://localhost:8000/submit-query', { query });
      
      // Get recommendations
      const response = await axios.get('http://localhost:8000/recommendations');
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBookmark = async (course: Course) => {
    try {
      await axios.post('http://localhost:8000/bookmark', course);
      alert('Course bookmarked successfully!');
    } catch (error) {
      console.error('Error bookmarking course:', error);
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

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700">
            What would you like to learn?
          </label>
          <input
            type="text"
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., I want to learn data science"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Find Courses'}
        </button>
      </form>

      <div className="space-y-4">
        {courses.map((course) => (
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
                onClick={() => handleBookmark(course)}
                className="text-gray-600 hover:text-gray-800"
              >
                Bookmark
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home; 
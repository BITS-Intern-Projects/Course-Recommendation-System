import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Bookmarks from './pages/Bookmarks';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-lg">
          <div className="max-w-6xl mx-auto px-4">
            <div className="flex justify-between">
              <div className="flex space-x-7">
                <div className="flex items-center py-4">
                  <span className="font-semibold text-gray-500 text-lg">Course Recommender</span>
                </div>
                <div className="hidden md:flex items-center space-x-1">
                  <Link to="/" className="py-4 px-2 text-gray-500 hover:text-blue-500 transition duration-300">Home</Link>
                  <Link to="/bookmarks" className="py-4 px-2 text-gray-500 hover:text-blue-500 transition duration-300">Bookmarks</Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-6xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/bookmarks" element={<Bookmarks />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App; 
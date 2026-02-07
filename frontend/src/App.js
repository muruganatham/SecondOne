import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import MainLayout from './Components/Layout/MainLayout';
import Dashboard from './pages/Dashboard';
import ChatUI from './pages/ChatUI';
import SuperAdmin from './pages/SuperAdmin';
import Leaderboard from './pages/Leaderboard';
import Login from './Components/Login';

// Helper component to conditionally render layout (e.g. skip for Login)
const AppLayout = ({ children }) => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const isChatPage = location.pathname === '/chat';

  // Skip layout entirely for login and chat pages
  if (isLoginPage || isChatPage) {
    return children;
  }

  return (
    <MainLayout>
      {children}
    </MainLayout>
  );
};

// ProtectedRoute component to check auth state dynamically
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('token');
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/chat"
            element={
              <ProtectedRoute>
                <ChatUI />
              </ProtectedRoute>
            }
          />
          <Route
            path="/super-admin"
            element={
              <ProtectedRoute>
                <SuperAdmin />
              </ProtectedRoute>
            }
          />
          <Route
            path="/leaderboard"
            element={
              <ProtectedRoute>
                <Leaderboard />
              </ProtectedRoute>
            }
          />
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;

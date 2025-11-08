import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, User, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

const ModernNavbar = ({ user }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-700 text-white shadow-xl">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="flex items-center gap-3"
          >
            <div className="bg-white/20 backdrop-blur-sm p-2 rounded-xl">
              <Sparkles size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">AI Placement Portal</h1>
              <p className="text-xs text-blue-100">Powered by Intelligent Matching</p>
            </div>
          </motion.div>

          {/* User Info */}
          <motion.div
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="flex items-center gap-4"
          >
            <div className="glass text-white px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-white/20 p-2 rounded-lg">
                <User size={20} />
              </div>
              <div className="text-left">
                <p className="font-semibold">{user?.name || user?.email}</p>
                <p className="text-xs opacity-90">{user?.role?.toUpperCase()}</p>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLogout}
              className="flex items-center gap-2 px-5 py-2.5 bg-red-500 hover:bg-red-600 rounded-xl font-semibold shadow-lg"
            >
              <LogOut size={18} />
              Logout
            </motion.button>
          </motion.div>
        </div>
      </div>
    </nav>
  );
};

export default ModernNavbar;

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, LogOut, Settings } from 'lucide-react';
import useAuthStore from '../store/authStore';

const Header = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const { user, logout } = useAuthStore();
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? 'text-primary-600' : 'text-gray-700';

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold text-primary-600">
            Ministry Operations
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link to="/schools" className={`${isActive('/schools')} hover:text-primary-600 transition`}>
              Schools
            </Link>
            <Link to="/inspections" className={`${isActive('/inspections')} hover:text-primary-600 transition`}>
              Inspections
            </Link>
            <Link to="/complaints" className={`${isActive('/complaints')} hover:text-primary-600 transition`}>
              Complaints
            </Link>
            <Link to="/resources" className={`${isActive('/resources')} hover:text-primary-600 transition`}>
              Resources
            </Link>
            <Link to="/field-visits" className={`${isActive('/field-visits')} hover:text-primary-600 transition`}>
              Field Visits
            </Link>
            <Link to="/tsc-services" className={`${isActive('/tsc-services')} hover:text-primary-600 transition`}>
              TSC Services
            </Link>
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="hidden md:flex items-center space-x-4">
                <span className="text-sm text-gray-700">{user.full_name}</span>
                <button
                  onClick={logout}
                  className="inline-flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-red-600 transition"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </button>
              </div>
            )}
            {/* Mobile menu button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <nav className="md:hidden pb-4 space-y-2">
            <Link to="/schools" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              Schools
            </Link>
            <Link to="/inspections" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              Inspections
            </Link>
            <Link to="/complaints" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              Complaints
            </Link>
            <Link to="/resources" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              Resources
            </Link>
            <Link to="/field-visits" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              Field Visits
            </Link>
            <Link to="/tsc-services" className="block px-3 py-2 rounded-md text-gray-700 hover:bg-primary-50">
              TSC Services
            </Link>
            {user && (
              <button
                onClick={() => {
                  logout();
                  setIsOpen(false);
                }}
                className="w-full text-left px-3 py-2 rounded-md text-gray-700 hover:bg-red-50 hover:text-red-600"
              >
                Logout
              </button>
            )}
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;

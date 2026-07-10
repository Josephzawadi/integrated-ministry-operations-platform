import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Input from '../components/Input';
import Button from '../components/Button';
import Alert from '../components/Alert';
import { Mail, Lock } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [alert, setAlert] = useState(null);
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await login({ email, password });
      setAlert({ type: 'success', message: 'Login successful!' });
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.detail || 'Login failed',
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Welcome Back</h2>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        {alert && (
          <div className="mb-6">
            <Alert
              type={alert.type}
              message={alert.message}
              onClose={() => setAlert(null)}
            />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Email Address"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (errors.email) setErrors((prev) => ({ ...prev, email: '' }));
            }}
            error={errors.email}
            placeholder="john@example.com"
            required
          />

          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (errors.password) setErrors((prev) => ({ ...prev, password: '' }));
            }}
            error={errors.password}
            placeholder="••••••••"
            required
          />

          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input
                type="checkbox"
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <span className="ml-2 text-sm text-gray-700">Remember me</span>
            </label>
            <Link to="#" className="text-sm text-primary-600 hover:text-primary-700">
              Forgot password?
            </Link>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={isLoading}
            className="w-full mt-6"
          >
            Sign In
          </Button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          Don't have an account?{' '}
          <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;

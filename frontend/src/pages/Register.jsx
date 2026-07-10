import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuthStore from '../store/authStore';
import Input from '../components/Input';
import Button from '../components/Button';
import Alert from '../components/Alert';
import { Mail, Lock, User } from 'lucide-react';

const Register = () => {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirm_password: '',
    role: 'viewer',
  });
  const [errors, setErrors] = useState({});
  const [alert, setAlert] = useState(null);
  const { register, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
    if (!formData.full_name) newErrors.full_name = 'Full name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }
    if (formData.password && formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      const { confirm_password, ...registerData } = formData;
      await register(registerData);
      setAlert({ type: 'success', message: 'Registration successful! Redirecting to login...' });
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      setAlert({ type: 'error', message: error.response?.data?.detail || 'Registration failed' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Create Account</h2>
          <p className="text-gray-600 mt-2">Join the Ministry Operations Platform</p>
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
            label="Full Name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            error={errors.full_name}
            placeholder="John Doe"
            required
          />

          <Input
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            placeholder="john@example.com"
            required
          />

          <Input
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            placeholder="••••••••"
            required
          />

          <Input
            label="Confirm Password"
            name="confirm_password"
            type="password"
            value={formData.confirm_password}
            onChange={handleChange}
            error={errors.confirm_password}
            placeholder="••••••••"
            required
          />

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="viewer">Viewer</option>
              <option value="data_analyst">Data Analyst</option>
              <option value="support_staff">Support Staff</option>
              <option value="inspector">Inspector</option>
              <option value="principal">Principal</option>
              <option value="ministry_official">Ministry Official</option>
              <option value="tsc_official">TSC Official</option>
            </select>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={isLoading}
            className="w-full mt-6"
          >
            Create Account
          </Button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;

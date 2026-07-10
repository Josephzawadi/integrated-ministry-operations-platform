import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';
import { ArrowRight, BarChart3, Zap, Shield } from 'lucide-react';

const Home = () => {
  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-primary-50 to-primary-100">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Integrated Ministry Operations Platform
          </h1>
          <p className="text-xl text-gray-700 mb-8">
            Unified platform for managing educational institutions, inspections, complaints, and TSC services
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button variant="primary" size="lg">
                Get Started <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="outline" size="lg">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <Shield className="w-12 h-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold mb-2">School Management</h3>
              <p className="text-gray-600">Register, manage, and track all educational institutions in one centralized system.</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <Zap className="w-12 h-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold mb-2">Inspections & Compliance</h3>
              <p className="text-gray-600">Schedule, conduct, and track school inspections with detailed compliance reports.</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <BarChart3 className="w-12 h-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold mb-2">Analytics & Reporting</h3>
              <p className="text-gray-600">Generate comprehensive reports and analytics on school performance and operations.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Modules Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">8 Integrated Modules</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              'Schools Management',
              'Inspections',
              'Complaints',
              'Data Collection',
              'Resources',
              'Field Visits',
              'TSC Services',
              'Document Registry',
            ].map((module) => (
              <div key={module} className="bg-white rounded-lg shadow-md p-4">
                <p className="font-semibold text-gray-900">{module}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4">
        <div className="max-w-2xl mx-auto text-center bg-primary-600 text-white rounded-lg p-12">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-lg mb-8">Join the Ministry Operations Platform and streamline your educational operations today.</p>
          <Link to="/register">
            <Button variant="primary" size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
              Create Account Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;

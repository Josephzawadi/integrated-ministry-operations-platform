import React, { useState, useEffect } from 'react';
import useAuthStore from '../store/authStore';
import Card from '../components/Card';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import { Users, FileText, CheckCircle, AlertCircle } from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuthStore();
  const [stats, setStats] = useState({
    totalSchools: 0,
    activeInspections: 0,
    pendingComplaints: 0,
    resourcesAllocated: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading stats
    setTimeout(() => {
      setStats({
        totalSchools: 1250,
        activeInspections: 45,
        pendingComplaints: 12,
        resourcesAllocated: 8750,
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Schools',
      value: stats.totalSchools,
      icon: Users,
      color: 'bg-blue-50 text-blue-600',
    },
    {
      title: 'Active Inspections',
      value: stats.activeInspections,
      icon: CheckCircle,
      color: 'bg-green-50 text-green-600',
    },
    {
      title: 'Pending Complaints',
      value: stats.pendingComplaints,
      icon: AlertCircle,
      color: 'bg-red-50 text-red-600',
    },
    {
      title: 'Resources Allocated',
      value: stats.resourcesAllocated,
      icon: FileText,
      color: 'bg-purple-50 text-purple-600',
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Welcome, {user?.full_name}!</h1>
        <p className="text-gray-600 mt-2">Here's what's happening in your Ministry Operations Platform</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Button variant="outline">Register New School</Button>
          <Button variant="outline">Schedule Inspection</Button>
          <Button variant="outline">File Complaint</Button>
          <Button variant="outline">View Reports</Button>
          <Button variant="outline">Manage Resources</Button>
          <Button variant="outline">Field Visits</Button>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card>
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {[1, 2, 3].map((item) => (
            <div key={item} className="flex items-center justify-between border-b pb-4 last:border-b-0">
              <div>
                <p className="font-medium text-gray-900">Activity Item {item}</p>
                <p className="text-sm text-gray-600">Description of the recent activity</p>
              </div>
              <span className="text-xs text-gray-500">2 hours ago</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;

import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, AlertCircle } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Input from '../components/Input';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { complaintsAPI, schoolsAPI } from '../api/endpoints';

const Complaints = () => {
  const [complaints, setComplaints] = useState([]);
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [formData, setFormData] = useState({
    school_id: '',
    subject: '',
    description: '',
    complainant_name: '',
    status: 'open',
    resolution: '',
  });

  useEffect(() => {
    fetchComplaintsAndSchools();
  }, []);

  const fetchComplaintsAndSchools = async () => {
    try {
      setLoading(true);
      const [complaintsRes, schoolsRes] = await Promise.all([
        complaintsAPI.list(),
        schoolsAPI.list(),
      ]);
      setComplaints(complaintsRes.data);
      setSchools(schoolsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (complaint = null) => {
    if (complaint) {
      setSelectedComplaint(complaint);
      setFormData(complaint);
    } else {
      setSelectedComplaint(null);
      setFormData({
        school_id: '',
        subject: '',
        description: '',
        complainant_name: '',
        status: 'open',
        resolution: '',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedComplaint(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedComplaint) {
        await complaintsAPI.update(selectedComplaint.id, formData);
      } else {
        await complaintsAPI.create(formData);
      }
      await fetchComplaintsAndSchools();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save complaint');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await complaintsAPI.delete(id);
        await fetchComplaintsAndSchools();
      } catch (err) {
        setError('Failed to delete complaint');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Complaint Management</h1>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          File Complaint
        </Button>
      </div>

      {error && (
        <Alert type="error" message={error} onClose={() => setError(null)} />
      )}

      <div className="grid grid-cols-1 gap-6">
        {complaints.map((complaint) => {
          const school = schools.find((s) => s.id === complaint.school_id);
          return (
            <Card key={complaint.id}>
              <div className="flex justify-between items-start">
                <div className="flex-grow">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {complaint.subject}
                    </h3>
                    {complaint.status === 'open' && (
                      <AlertCircle className="w-5 h-5 text-red-600" />
                    )}
                  </div>
                  <p className="text-gray-600 mt-1">{school?.name}</p>
                  <p className="text-sm text-gray-600 mt-2">{complaint.description}</p>
                  <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Complainant</p>
                      <p className="font-medium">{complaint.complainant_name}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Status</p>
                      <p className="font-medium capitalize">{complaint.status}</p>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleOpenModal(complaint)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(complaint.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <Modal
        isOpen={showModal}
        title={selectedComplaint ? 'Edit Complaint' : 'File Complaint'}
        onClose={handleCloseModal}
        footerContent={
          <>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              {selectedComplaint ? 'Update' : 'File'}
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              School
            </label>
            <select
              value={formData.school_id}
              onChange={(e) => setFormData({ ...formData, school_id: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select school</option>
              {schools.map((school) => (
                <option key={school.id} value={school.id}>
                  {school.name}
                </option>
              ))}
            </select>
          </div>
          <Input
            label="Subject"
            value={formData.subject}
            onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
            placeholder="Complaint subject"
            required
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Detailed description"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="4"
            />
          </div>
          <Input
            label="Complainant Name"
            value={formData.complainant_name}
            onChange={(e) => setFormData({ ...formData, complainant_name: e.target.value })}
            placeholder="Your name"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Resolution
            </label>
            <textarea
              value={formData.resolution}
              onChange={(e) => setFormData({ ...formData, resolution: e.target.value })}
              placeholder="Resolution details"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="3"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Complaints;

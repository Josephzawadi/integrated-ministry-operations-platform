import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, CheckCircle, Clock } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Input from '../components/Input';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { inspectionsAPI, schoolsAPI } from '../api/endpoints';

const Inspections = () => {
  const [inspections, setInspections] = useState([]);
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedInspection, setSelectedInspection] = useState(null);
  const [formData, setFormData] = useState({
    school_id: '',
    inspector_id: '',
    inspection_date: '',
    status: 'scheduled',
    findings: '',
    recommendations: '',
  });

  useEffect(() => {
    fetchInspectionsAndSchools();
  }, []);

  const fetchInspectionsAndSchools = async () => {
    try {
      setLoading(true);
      const [inspectionsRes, schoolsRes] = await Promise.all([
        inspectionsAPI.list(),
        schoolsAPI.list(),
      ]);
      setInspections(inspectionsRes.data);
      setSchools(schoolsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (inspection = null) => {
    if (inspection) {
      setSelectedInspection(inspection);
      setFormData(inspection);
    } else {
      setSelectedInspection(null);
      setFormData({
        school_id: '',
        inspector_id: '',
        inspection_date: '',
        status: 'scheduled',
        findings: '',
        recommendations: '',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedInspection(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedInspection) {
        await inspectionsAPI.update(selectedInspection.id, formData);
      } else {
        await inspectionsAPI.create(formData);
      }
      await fetchInspectionsAndSchools();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save inspection');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await inspectionsAPI.delete(id);
        await fetchInspectionsAndSchools();
      } catch (err) {
        setError('Failed to delete inspection');
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

  const getStatusIcon = (status) => {
    return status === 'completed' ? (
      <CheckCircle className="w-5 h-5 text-green-600" />
    ) : (
      <Clock className="w-5 h-5 text-yellow-600" />
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">School Inspections</h1>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          Schedule Inspection
        </Button>
      </div>

      {error && (
        <Alert type="error" message={error} onClose={() => setError(null)} />
      )}

      <div className="grid grid-cols-1 gap-6">
        {inspections.map((inspection) => {
          const school = schools.find((s) => s.id === inspection.school_id);
          return (
            <Card key={inspection.id}>
              <div className="flex justify-between items-start">
                <div className="flex-grow">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {school?.name}
                    </h3>
                    {getStatusIcon(inspection.status)}
                  </div>
                  <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Date</p>
                      <p className="font-medium">{inspection.inspection_date}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Status</p>
                      <p className="font-medium capitalize">{inspection.status}</p>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleOpenModal(inspection)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(inspection.id)}
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
        title={selectedInspection ? 'Edit Inspection' : 'Schedule Inspection'}
        onClose={handleCloseModal}
        footerContent={
          <>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              {selectedInspection ? 'Update' : 'Schedule'}
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
            label="Inspection Date"
            type="date"
            value={formData.inspection_date}
            onChange={(e) => setFormData({ ...formData, inspection_date: e.target.value })}
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
              <option value="scheduled">Scheduled</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Findings
            </label>
            <textarea
              value={formData.findings}
              onChange={(e) => setFormData({ ...formData, findings: e.target.value })}
              placeholder="Enter inspection findings"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="4"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recommendations
            </label>
            <textarea
              value={formData.recommendations}
              onChange={(e) => setFormData({ ...formData, recommendations: e.target.value })}
              placeholder="Enter recommendations"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="4"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Inspections;

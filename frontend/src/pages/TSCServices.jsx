import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, FileText } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Input from '../components/Input';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { tscServicesAPI, schoolsAPI } from '../api/endpoints';

const TSCServices = () => {
  const [services, setServices] = useState([]);
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedService, setSelectedService] = useState(null);
  const [formData, setFormData] = useState({
    school_id: '',
    requested_by_id: '',
    service_type: '',
    request_date: '',
    status: 'pending',
    description: '',
  });

  useEffect(() => {
    fetchServicesAndSchools();
  }, []);

  const fetchServicesAndSchools = async () => {
    try {
      setLoading(true);
      const [servicesRes, schoolsRes] = await Promise.all([
        tscServicesAPI.list(),
        schoolsAPI.list(),
      ]);
      setServices(servicesRes.data);
      setSchools(schoolsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (service = null) => {
    if (service) {
      setSelectedService(service);
      setFormData(service);
    } else {
      setSelectedService(null);
      setFormData({
        school_id: '',
        requested_by_id: '',
        service_type: '',
        request_date: '',
        status: 'pending',
        description: '',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedService(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedService) {
        await tscServicesAPI.update(selectedService.id, formData);
      } else {
        await tscServicesAPI.create(formData);
      }
      await fetchServicesAndSchools();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save service');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await tscServicesAPI.delete(id);
        await fetchServicesAndSchools();
      } catch (err) {
        setError('Failed to delete service');
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
        <h1 className="text-3xl font-bold text-gray-900">TSC Services</h1>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          New Request
        </Button>
      </div>

      {error && (
        <Alert type="error" message={error} onClose={() => setError(null)} />
      )}

      <div className="grid grid-cols-1 gap-6">
        {services.map((service) => {
          const school = schools.find((s) => s.id === service.school_id);
          return (
            <Card key={service.id}>
              <div className="flex justify-between items-start">
                <div className="flex-grow">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-purple-600" />
                    <h3 className="text-lg font-semibold text-gray-900">
                      {service.service_type}
                    </h3>
                  </div>
                  <p className="text-gray-600 mt-1">{school?.name}</p>
                  <p className="text-sm text-gray-600 mt-1">{service.description}</p>
                  <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Reference</p>
                      <p className="font-medium">{service.tsc_reference_number}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Status</p>
                      <p className="font-medium capitalize">{service.status}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Request Date</p>
                      <p className="font-medium">{service.request_date}</p>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleOpenModal(service)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(service.id)}
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
        title={selectedService ? 'Edit TSC Service' : 'New TSC Service Request'}
        onClose={handleCloseModal}
        footerContent={
          <>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              {selectedService ? 'Update' : 'Submit'}
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
            label="Service Type"
            value={formData.service_type}
            onChange={(e) => setFormData({ ...formData, service_type: e.target.value })}
            placeholder="e.g., Teacher Certification, Payroll"
            required
          />
          <Input
            label="Request Date"
            type="date"
            value={formData.request_date}
            onChange={(e) => setFormData({ ...formData, request_date: e.target.value })}
            required
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
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Service description"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="3"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default TSCServices;

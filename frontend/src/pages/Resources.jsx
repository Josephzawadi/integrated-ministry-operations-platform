import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2 } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Input from '../components/Input';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { resourcesAPI, schoolsAPI } from '../api/endpoints';

const Resources = () => {
  const [resources, setResources] = useState([]);
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedResource, setSelectedResource] = useState(null);
  const [formData, setFormData] = useState({
    school_id: '',
    resource_type: '',
    quantity: '',
    allocation_date: '',
    status: 'pending',
    notes: '',
  });

  useEffect(() => {
    fetchResourcesAndSchools();
  }, []);

  const fetchResourcesAndSchools = async () => {
    try {
      setLoading(true);
      const [resourcesRes, schoolsRes] = await Promise.all([
        resourcesAPI.list(),
        schoolsAPI.list(),
      ]);
      setResources(resourcesRes.data);
      setSchools(schoolsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (resource = null) => {
    if (resource) {
      setSelectedResource(resource);
      setFormData(resource);
    } else {
      setSelectedResource(null);
      setFormData({
        school_id: '',
        resource_type: '',
        quantity: '',
        allocation_date: '',
        status: 'pending',
        notes: '',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedResource(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedResource) {
        await resourcesAPI.update(selectedResource.id, formData);
      } else {
        await resourcesAPI.create(formData);
      }
      await fetchResourcesAndSchools();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save resource');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await resourcesAPI.delete(id);
        await fetchResourcesAndSchools();
      } catch (err) {
        setError('Failed to delete resource');
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
        <h1 className="text-3xl font-bold text-gray-900">Resource Distribution</h1>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          Allocate Resource
        </Button>
      </div>

      {error && (
        <Alert type="error" message={error} onClose={() => setError(null)} />
      )}

      <div className="grid grid-cols-1 gap-6">
        {resources.map((resource) => {
          const school = schools.find((s) => s.id === resource.school_id);
          return (
            <Card key={resource.id}>
              <div className="flex justify-between items-start">
                <div className="flex-grow">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {resource.resource_type}
                  </h3>
                  <p className="text-gray-600 mt-1">{school?.name}</p>
                  <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Quantity</p>
                      <p className="font-medium">{resource.quantity}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Allocation Date</p>
                      <p className="font-medium">{resource.allocation_date}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Status</p>
                      <p className="font-medium capitalize">{resource.status}</p>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleOpenModal(resource)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(resource.id)}
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
        title={selectedResource ? 'Edit Resource' : 'Allocate Resource'}
        onClose={handleCloseModal}
        footerContent={
          <>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              {selectedResource ? 'Update' : 'Allocate'}
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
            label="Resource Type"
            value={formData.resource_type}
            onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
            placeholder="e.g., Computers, Books, Furniture"
            required
          />
          <Input
            label="Quantity"
            type="number"
            value={formData.quantity}
            onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
            placeholder="Enter quantity"
            required
          />
          <Input
            label="Allocation Date"
            type="date"
            value={formData.allocation_date}
            onChange={(e) => setFormData({ ...formData, allocation_date: e.target.value })}
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
              <option value="allocated">Allocated</option>
              <option value="delivered">Delivered</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes
            </label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="Additional notes"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="3"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Resources;

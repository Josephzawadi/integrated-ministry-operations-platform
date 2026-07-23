import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import Modal from '../components/Modal';
import Input from '../components/Input';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';
import { schoolsAPI } from '../api/endpoints';

const emptyForm = {
  name: '',
  registration_number: '',
  county: '',
  subcounty: '',
  constituency: '',
  school_type: '',
  contact_person: '',
  contact_phone: '',
  contact_email: '',
};

const Schools = () => {
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedSchool, setSelectedSchool] = useState(null);
  const [formData, setFormData] = useState(emptyForm);

  useEffect(() => {
    fetchSchools();
  }, []);

  const fetchSchools = async () => {
    try {
      setLoading(true);
      const response = await schoolsAPI.list();
      setSchools(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch schools');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (school = null) => {
    if (school) {
      setSelectedSchool(school);
      setFormData({
        name: school.name || '',
        registration_number: school.registration_number || '',
        county: school.county || '',
        subcounty: school.subcounty || '',
        constituency: school.constituency || '',
        school_type: school.school_type || '',
        contact_person: school.contact_person || '',
        contact_phone: school.contact_phone || '',
        contact_email: school.contact_email || '',
      });
    } else {
      setSelectedSchool(null);
      setFormData(emptyForm);
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedSchool(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedSchool) {
        await schoolsAPI.update(selectedSchool.id, formData);
      } else {
        await schoolsAPI.create(formData);
      }
      setError(null);
      await fetchSchools();
      handleCloseModal();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save school');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this school?')) {
      try {
        await schoolsAPI.delete(id);
        await fetchSchools();
      } catch (err) {
        setError('Failed to delete school');
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
        <h1 className="text-3xl font-bold text-gray-900">Schools Management</h1>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <Plus className="w-4 h-4 mr-2" />
          Add School
        </Button>
      </div>

      {error && (
        <Alert type="error" message={error} onClose={() => setError(null)} />
      )}

      <div className="grid grid-cols-1 gap-6">
        {schools.map((school) => (
          <Card key={school.id}>
            <div className="flex justify-between items-start">
              <div className="flex-grow">
                <h3 className="text-lg font-semibold text-gray-900">{school.name}</h3>
                <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Registration</p>
                    <p className="font-medium">{school.registration_number}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">County</p>
                    <p className="font-medium">{school.county}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Type</p>
                    <p className="font-medium">{school.school_type}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Contact Person</p>
                    <p className="font-medium">{school.contact_person || '—'}</p>
                  </div>
                </div>
              </div>
              <div className="flex space-x-2">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleOpenModal(school)}
                >
                  <Edit className="w-4 h-4" />
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => handleDelete(school.id)}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Modal
        isOpen={showModal}
        title={selectedSchool ? 'Edit School' : 'Add New School'}
        onClose={handleCloseModal}
        footerContent={
          <>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              {selectedSchool ? 'Update' : 'Create'}
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <Input
            label="School Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Enter school name"
            required
          />
          <Input
            label="Registration Number"
            value={formData.registration_number}
            onChange={(e) => setFormData({ ...formData, registration_number: e.target.value })}
            placeholder="e.g., REG-001"
            required
          />
          <Input
            label="County"
            value={formData.county}
            onChange={(e) => setFormData({ ...formData, county: e.target.value })}
            placeholder="Enter county"
            required
          />
          <Input
            label="Subcounty"
            value={formData.subcounty}
            onChange={(e) => setFormData({ ...formData, subcounty: e.target.value })}
            placeholder="Enter subcounty"
            required
          />
          <Input
            label="Constituency"
            value={formData.constituency}
            onChange={(e) => setFormData({ ...formData, constituency: e.target.value })}
            placeholder="Enter constituency"
            required
          />
          <Input
            label="School Type"
            value={formData.school_type}
            onChange={(e) => setFormData({ ...formData, school_type: e.target.value })}
            placeholder="e.g., Primary, Secondary"
            required
          />
          <Input
            label="Contact Person"
            value={formData.contact_person}
            onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })}
            placeholder="Enter contact person name"
          />
          <Input
            label="Contact Phone"
            value={formData.contact_phone}
            onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
            placeholder="Enter phone number"
          />
          <Input
            label="Contact Email"
            type="email"
            value={formData.contact_email}
            onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
            placeholder="Enter contact email"
          />
        </div>
      </Modal>
    </div>
  );
};

export default Schools;
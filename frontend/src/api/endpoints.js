import api from './client';

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
};

export const schoolsAPI = {
  create: (data) => api.post('/schools/', data),
  list: (params) => api.get('/schools/', { params }),
  get: (id) => api.get(`/schools/${id}`),
  update: (id, data) => api.patch(`/schools/${id}`, data),
  delete: (id) => api.delete(`/schools/${id}`),
};

export const inspectionsAPI = {
  create: (data) => api.post('/inspections/', data),
  list: (params) => api.get('/inspections/', { params }),
  get: (id) => api.get(`/inspections/${id}`),
  update: (id, data) => api.patch(`/inspections/${id}`, data),
  delete: (id) => api.delete(`/inspections/${id}`),
};

export const complaintsAPI = {
  create: (data) => api.post('/complaints/', data),
  list: (params) => api.get('/complaints/', { params }),
  get: (id) => api.get(`/complaints/${id}`),
  update: (id, data) => api.patch(`/complaints/${id}`, data),
  delete: (id) => api.delete(`/complaints/${id}`),
};

export const schoolDataAPI = {
  create: (data) => api.post('/school-data/', data),
  list: (params) => api.get('/school-data/', { params }),
  get: (id) => api.get(`/school-data/${id}`),
  getBySchool: (schoolId) => api.get(`/school-data/school/${schoolId}`),
  update: (id, data) => api.patch(`/school-data/${id}`, data),
  delete: (id) => api.delete(`/school-data/${id}`),
};

export const resourcesAPI = {
  create: (data) => api.post('/resources/', data),
  list: (params) => api.get('/resources/', { params }),
  get: (id) => api.get(`/resources/${id}`),
  getBySchool: (schoolId, params) => api.get(`/resources/school/${schoolId}`, { params }),
  update: (id, data) => api.patch(`/resources/${id}`, data),
  delete: (id) => api.delete(`/resources/${id}`),
};

export const fieldVisitsAPI = {
  create: (data) => api.post('/field-visits/', data),
  list: (params) => api.get('/field-visits/', { params }),
  get: (id) => api.get(`/field-visits/${id}`),
  update: (id, data) => api.patch(`/field-visits/${id}`, data),
  delete: (id) => api.delete(`/field-visits/${id}`),
};

export const tscServicesAPI = {
  create: (data) => api.post('/tsc-services/', data),
  list: (params) => api.get('/tsc-services/', { params }),
  get: (id) => api.get(`/tsc-services/${id}`),
  update: (id, data) => api.patch(`/tsc-services/${id}`, data),
  delete: (id) => api.delete(`/tsc-services/${id}`),
};

export const registryAPI = {
  create: (data) => api.post('/registry/', data),
  list: (params) => api.get('/registry/', { params }),
  get: (id) => api.get(`/registry/${id}`),
  update: (id, data) => api.patch(`/registry/${id}`, data),
  delete: (id) => api.delete(`/registry/${id}`),
};

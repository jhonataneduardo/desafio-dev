import api from '../lib/api';

export const cnabService = {

  async uploadCnab(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/transactions/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

};

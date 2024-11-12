import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatWithAI = async ({ query }: { query: string; }) => {
  try {
    const response = await api.post('/chat/', { query });
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error chatting with AI:', error);
    throw error;
  }
};

export const uploadFile = async (files: File[]) => {
  try {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });
    const response = await api.post('/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading files:', error);
    throw error;
  }
};
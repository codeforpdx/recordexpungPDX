import apiService, { Request } from './api-service';

const request: Request = {
  url: 'http://localhost:5000/api/search',
  method: 'post'
};

export default function getSearchRecords() {
  return apiService(request);
}

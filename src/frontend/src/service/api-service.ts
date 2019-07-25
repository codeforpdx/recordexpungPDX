import axios from 'axios';

enum MethodOptions {
  post = 'post',
  get = 'get',
  delete = 'delete',
  head = 'head',
  put = 'put',
  patch = 'patch'
}

type Request = {
  url: string;
  data?: object;
  method: MethodOptions;
};

export default function apiService(request: Request) {
  return axios
    .request(request)
    .then(res => [res.statusText, res.data, res.status])
    .then(([statusText, data, status]) => {
      if (statusText) {
        return {
          data,
          status,
          statusText
        };
      }
    })
    .catch(e => {
      return {
        error: e.message
      };
    });
}

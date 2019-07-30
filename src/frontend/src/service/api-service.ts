import axios from 'axios';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

export type Request = {
  url: string;
  data?: object;
  method: Method;
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

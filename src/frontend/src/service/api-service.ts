import axios from 'axios';

type MethodOptions =
  | 'POST'
  | 'post'
  | 'GET'
  | 'get'
  | 'DELETE'
  | 'delete'
  | 'head'
  | 'HEAD'
  | 'put'
  | 'PUT'
  | 'patch'
  | 'PATCH';

type Req = {
  url: string;
  data?: object;
  method: MethodOptions;
};

export default function apiService(req: Req) {
  return axios
    .request(req)
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

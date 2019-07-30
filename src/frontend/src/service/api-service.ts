import axios from 'axios';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

export type Request = {
  url: string;
  data?: object;
  method: Method;
};

type Response = {
  statusText?: string;
  data?: object;
  status?: number;
  error?: Error;
};

export default function apiService(request: Request) {
  return axios
    .request(request)
    .then((response: Response) => {
      return {
        data: response.data,
        status: response.status,
        statusText: response.statusText
      };
    })
    .catch(error => error);
}

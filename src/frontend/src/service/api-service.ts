import axios from 'axios';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

// optionally pass in main authToken: this.props.system.authToken
// or oeciToken: this.props.systen.oeciToken
// token not required for every request
export type Request = {
  url: string;
  data?: object;
  method: Method;
  headers?: {
    Authorization: string;
  };
};

export default function apiService(request: Request) {
  return axios.request(request);
}

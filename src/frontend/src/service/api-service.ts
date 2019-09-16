import axios from 'axios';

type Method = 'post' | 'delete' | 'get' | 'head' | 'delete' | 'options' | 'put';

// we can use either the main authToken or oeciToken depending on endpoint
// accessed via SystemState not required for every request
type AuthToken = 'this.props.authToken' | 'this.props.oeciToken';

export type Request = {
  url: string;
  data?: object;
  method: Method;
  headers?: {
    [Authorization: string]: AuthToken;
  };
};

export default function apiService(request: Request) {
  return axios.request(request);
}

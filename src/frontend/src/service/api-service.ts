import axios, { AxiosPromise, AxiosRequestConfig } from 'axios';

export default function apiService<T>(
  dispatch: Function,
  request: AxiosRequestConfig
): AxiosPromise {
  return axios.request<T>(request).catch(error => {
    return Promise.reject(error);
  });
}

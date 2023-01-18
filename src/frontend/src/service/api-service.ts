import axios, { AxiosPromise, RawAxiosRequestConfig } from "axios";

export default function apiService(
  dispatch: Function,
  request: RawAxiosRequestConfig
): AxiosPromise {
  return axios.request(request).catch((error) => {
    return Promise.reject(error);
  });
}

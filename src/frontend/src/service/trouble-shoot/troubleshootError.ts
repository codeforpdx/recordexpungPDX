import axios from 'axios';

enum MethodOptionsPascalCaseEnum {
  Post = 'post',
  Get = 'get',
  Delete = 'delete',
  Head = 'head',
  Put = 'put',
  Patch = 'patch'
}
type RequestPascalCaseEnum = {
  url: string;
  data?: object;
  method: MethodOptionsPascalCaseEnum;
};

enum MethodOptionsCamelCaseEnum {
  post = 'post',
  get = 'get',
  delete = 'delete',
  head = 'head',
  put = 'put',
  patch = 'patch'
}
type RequestCamelCaseEnum = {
  url: string;
  data?: object;
  method: MethodOptionsCamelCaseEnum;
};

export function apiServiceEnumPascalCase(request: RequestPascalCaseEnum) {
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

export function apiServiceEnumCamelCase(request: RequestCamelCaseEnum) {
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

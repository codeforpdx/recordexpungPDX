import {
  apiServiceEnumPascalCase,
  apiServiceEnumCamelCase
} from './troubleshootError';

/*
AXIOS METHODS:'post', 'POST','get', 'GET', 'delete', 'DELETE', 'head', 'HEAD',
'put', 'PUT,'patch', 'PATCH'.
*/

describe(`Axios is willing to take the defined methods seen above as string, this works
when not checking types, however with typescript, type check will fail`, () => {
  it(`Try defining input types with enums declared in PascalCase.
      Expected behavior: type check passes.
      Observed behavior: type string is not assigneable to type 'MethodOptions
  `, () => {
    const request = {
      url: 'http://localhost:5000/api/hello',
      method: 'post'
    };
    apiServiceEnumPascalCase(request)
      /*
    TYPESCRIPT ERROR FOR REQUEST IS BELOW
    Argument of type '{ url: string; method: string; }' is not assignable to parameter of type 'Request'.
  Types of property 'method' are incompatible.
    Type 'string' is not assignable to type 'MethodOptions'.ts(2345)
    */
      .then(response => {
        expect(response).toEqual({
          data: 'Hello, world!',
          status: 200,
          statusText: 'OK'
        });
      });
  });
  it(`
      Try defining input types with enums declared in camelCase.
      Expected behavior: type check passes.
      Observed behavior: type string is not assigneable to type 'MethodOptions
  `, () => {
    const request = {
      url: 'http://localhost:5000/api/hello',
      method: 'post'
    };
    apiServiceEnumCamelCase(request)
      /*
    TYPESCRIPT ERROR FOR REQUEST IS BELOW
  Argument of type '{ url: string; method: string; }' is not assignable to parameter of type 'Request'.
  Types of property 'method' are incompatible.
    Type 'string' is not assignable to type 'MethodOptions'.ts(2345)
    */
      .then(response => {
        expect(response).toEqual({
          data: 'Hello, world!',
          status: 200,
          statusText: 'OK'
        });
      });
  });
});

interface Cookie {
  [key: string]: string;
}

const getKeyValue = (inputCookie: string) =>
  // splits the cookie-string on only the first '='
  [
    inputCookie.substring(0, inputCookie.indexOf('=')),
    inputCookie.substring(inputCookie.indexOf('=') + 1, inputCookie.length)
  ];

export function decodeCookie() {
  // first splits cookie into separate strings and then mapped to a returned object
  return document.cookie
    .split(';')
    .reduce((returnObject: Cookie, currentCookie) => {
      const [key, value] = getKeyValue(currentCookie);
      // trim whitespace off of 'key'
      returnObject[key.trim()] = value;
      return returnObject;
    }, {});
}

export function setLogInCookie(inputToken: string, inputId: string) {
  // 'max-age' is set to 1 hour
  document.cookie = `authToken=${inputToken}; max-age=36000;`;
  document.cookie = `userId=${inputId}; max-age=36000;`;
}

export function removeCookie() {
  document.cookie = 'authToken=; max-age=0;';
  document.cookie = 'userId=; max-age=0;';
  document.cookie = 'oeci_token=; max-age=0;';
}

export function hasOeciToken() {
  return decodeCookie().oeci_token ? true : false;
}

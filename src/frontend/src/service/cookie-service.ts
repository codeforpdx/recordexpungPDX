import history from '../service/history';

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

export function removeCookie() {
  document.cookie = 'remember_token=; max-age=0;';
  document.cookie = 'oeci_token=; max-age=0;';
}

export function hasOeciToken() {
  return decodeCookie().oeci_token ? true : false;
}

export function checkOeciRedirect() {
  if (!hasOeciToken()) {
    history.push('/oeci');
    alert('You must sign into the OECI database before performing a search.');
  }
}

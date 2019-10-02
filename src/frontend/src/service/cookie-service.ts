interface Cookie {
  auth_token: string;
  user_id: string;
}

export function decodeCookie() {
  // this decodes the cookie creating an object with {key: `value`} pairs
  // https://gist.github.com/rendro/525bbbf85e84fa9042c2#gistcomment-2784930
  const data: any = document.cookie.split(';').reduce((res, c) => {
    const [key, val] = c
      .trim()
      .split('=')
      .map(decodeURIComponent);
    const allNumbers = (str: string) => /^\d+$/.test(str);
    try {
      return Object.assign(res, {
        [key]: allNumbers(val) ? val : JSON.parse(val)
      });
    } catch (e) {
      return Object.assign(res, { [key]: val });
    }
  }, {});

  return data;
}

export function setCookie(cookie: Cookie) {
  document.cookie = `authToken=${cookie.auth_token}`;
  document.cookie = `userId=${cookie.user_id}`;
}

export function removeCookie() {
  document.cookie = 'authToken=';
  document.cookie = 'userId=';
}

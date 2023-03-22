import history from "../service/history";
import store, {clearAllData} from "../redux/store";

interface Cookie {
  [key: string]: string;
}

const getKeyValue = (inputCookie: string) => [
  inputCookie.substring(0, inputCookie.indexOf("=")),
  inputCookie.substring(inputCookie.indexOf("=") + 1, inputCookie.length),
];

export function decodeCookie() {
  return document.cookie
    .split(";")
    .reduce((returnObject: Cookie, currentCookie) => {
      const [key, value] = getKeyValue(currentCookie);
      returnObject[key.trim()] = value;
      return returnObject;
    }, {});
}

export function removeCookie() {
  document.cookie = "remember_token=; max-age=0;";
  document.cookie = "oeci_token=; max-age=0;";
  document.cookie = "is_admin=; max-age=0;";
}

export function hasOeciToken() {
  return decodeCookie().oeci_token ? true : false;
}

export function isAdmin() {
  return document.cookie.includes("is_admin");
}

export function checkOeciRedirect() {
  if (!hasOeciToken()) {
    history.replace("/oeci");
  }
}

export function isLoggedIn() {
  return hasOeciToken();
}

export function oeciLogout() {
  removeCookie();
  store.dispatch(clearAllData());
  history.replace("/oeci");
}


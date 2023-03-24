import apiService from "./api-service";
import { hasOeciToken } from "./cookie-service";
import history from "./history";
import store from "../redux/store";
import { setLoggedIn } from "../redux/authSlice";

export default function oeciLogIn(username: string, password: string): any {
  return apiService(() => {}, {
    url: "/api/oeci_login",
    data: { oeci_username: username, oeci_password: password },
    method: "post",
    withCredentials: true,
  }).then((response: any) => {
    if (hasOeciToken()) {
      store.dispatch(setLoggedIn(true));
      history.push("/record-search");
    }
  });
}

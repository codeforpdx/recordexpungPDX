import apiService from './api-service';
import { hasOeciToken } from './cookie-service';
import history from './history';

export default function oeciLogIn(username: string, password: string): any {
  return apiService(() => {}, {
    url: '/api/oeci_login',
    data: { oeci_username: username, oeci_password: password },
    method: 'post',
    withCredentials: true,
  }).then((response: any) => {
    if (hasOeciToken()) {
      history.push('/record-search');
    }
  });
}

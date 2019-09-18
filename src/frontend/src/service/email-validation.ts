export default function validateEmail(email: string) {
  // returns true if the email is correct format: https://www.w3resource.com/javascript/form/email-validation.php
  // empty or format != "_@_._" will return false
  return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(email);
}

import moment from "moment";

export function isValidWildcard(str: string, minLength: number): boolean {
  return str.endsWith("*") && str.length >= minLength;
}

export function isValidOptionalWildcard(str: string, minLength: number) {
  return !str.includes("*") || isValidWildcard(str, minLength);
}

export function isBlank(str: string) {
  return str.trim().length === 0;
}

export function areAnyBlank(...args: string[]) {
  return args.some(isBlank);
}

export function isValidDate(str: string, format = "M/D/YYYY") {
  return moment(str, format, true).isValid();
}

export function isValidOptionalDate(str: string, format = "M/D/YYYY") {
  return isBlank(str) || moment(str, format, true).isValid();
}

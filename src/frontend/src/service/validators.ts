import moment from "moment";

export type Validator<T> = (alias: T, index: number, array: T[]) => boolean;

type ValidatorMessageTuple<T> = [Validator<T>, string];

export function isBlank(str: string) {
  return str.trim().length === 0;
}

export function isDate(str: string, format = "M/D/YYYY") {
  return moment(str, format, true).isValid();
}

export function isValidWildcard(str: string, minLength = 2): boolean {
  return str.indexOf("*") === str.length - 1 && str.length >= minLength;
}

export function isPresent<T extends Record<string, any>>(
  attribute: keyof T,
  message: string
): ValidatorMessageTuple<T> {
  return [(obj: T) => !isBlank(obj[attribute]), message];
}

export function isValidOptionalDate<T extends Record<string, any>>(
  attribute: keyof T,
  message: string,
  opts = { format: "M/D/YYYY", indexes: undefined } as {
    format?: string;
    indexes?: number[];
  }
): ValidatorMessageTuple<T> {
  return [
    (obj: T, idx: number) =>
      (opts.indexes && !opts.indexes.includes(idx)) ||
      isBlank(obj[attribute]) ||
      isDate(obj[attribute], opts.format),
    message,
  ];
}

export function isValidOptionalWildcard<T extends Record<string, any>>(
  attribute: keyof T,
  message: string,
  opts = { minLength: 2 } as {
    minLength?: number;
  }
): ValidatorMessageTuple<T> {
  return [
    (obj: T) =>
      !obj[attribute].includes("*") ||
      isValidWildcard(obj[attribute], opts.minLength),
    message,
  ];
}

export function validate<T>(
  objs: T | T[],
  validators: ValidatorMessageTuple<T> | ValidatorMessageTuple<T>[],
  errorMessagesSetter: (messages: string[]) => void,
  onAllValid = () => {}
) {
  const objArray = Array.isArray(objs) ? objs : [objs];

  const validatorsArray = (
    Array.isArray(validators[0]) ? validators : [validators]
  ) as ValidatorMessageTuple<T>[];

  const errorMessages = validatorsArray.reduce((errors, [isValid, message]) => {
    if (!objArray.every(isValid)) errors.push(message);
    return errors;
  }, [] as string[]);

  const areAllVaid = errorMessages.length === 0;

  errorMessagesSetter(errorMessages);

  if (areAllVaid) onAllValid();
  return areAllVaid;
}

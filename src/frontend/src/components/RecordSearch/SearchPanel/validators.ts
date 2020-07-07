export function isValidWildcard(
  searchTerm: string,
  requiredLength: number
): boolean {
  if (searchTerm.length < requiredLength) {
    return false;
  } else if (searchTerm.indexOf("*") < searchTerm.length - 1) {
    return false;
  } else {
    return true;
  }
}

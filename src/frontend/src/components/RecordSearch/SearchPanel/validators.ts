export function isValidWildcard(searchTerm: string, firstOrLast: 'first' | 'last'): boolean {
  const requiredLength = firstOrLast === 'first' ? 2 : 3;

  if (searchTerm.length < requiredLength) return false;
  if (searchTerm.indexOf('*') < searchTerm.length - 1) return false;

  return true;
}
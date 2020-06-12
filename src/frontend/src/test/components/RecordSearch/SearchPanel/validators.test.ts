import { isValidWildcard } from '../../../../components/RecordSearch/SearchPanel/validators';

describe('#isValidWildcard', () => {
  it('requires 1 characters for first name', () => {
    expect(isValidWildcard('*', 'first')).toEqual(false);
    expect(isValidWildcard('a*', 'first')).toEqual(true);
  });

  it('requires 2 characters for last name', () => {
    expect(isValidWildcard('a*', 'last')).toEqual(false);
    expect(isValidWildcard('ab*', 'last')).toEqual(true);
  });

  it('requires that wildcard is at end of word', () => {
    expect(isValidWildcard('ab*c', 'last')).toEqual(false);
  });

  it('returns true for valid wildcards', () => {
    expect(isValidWildcard('hello*', 'last')).toEqual(true);
    expect(isValidWildcard('h*', 'first')).toEqual(true);
  })
});


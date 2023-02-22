import { isValidWildcard } from "../../../../service/validators";

describe("#isValidWildcard", () => {
  it("requires 1 characters for first name", () => {
    expect(isValidWildcard("*", 2)).toEqual(false);
    expect(isValidWildcard("a*", 2)).toEqual(true);
  });

  it("requires 2 characters for last name", () => {
    expect(isValidWildcard("a*", 3)).toEqual(false);
    expect(isValidWildcard("ab*", 3)).toEqual(true);
  });

  it("requires that wildcard is at end of word", () => {
    expect(isValidWildcard("ab*c", 3)).toEqual(false);
  });

  it("returns true for valid wildcards", () => {
    expect(isValidWildcard("hello*", 3)).toEqual(true);
    expect(isValidWildcard("h*", 2)).toEqual(true);
  });
});

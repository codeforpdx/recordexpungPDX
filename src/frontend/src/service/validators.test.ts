import { isDate } from "./validators";

describe("isDate", () => {
  test.each`
    input            | format           | expected
    ${"2/3/2002"}    | ${undefined}     | ${true}
    ${"1999"}        | ${"yyyy"}        | ${true}
    ${"Mar 3, 1977"} | ${undefined}     | ${false}
    ${"Mar 3, 1977"} | ${"MMM d, yyyy"} | ${true}
  `(
    'returns $expected for input "$input" with format "$format"',
    ({ input, format, expected }) => {
      expect(isDate(input, format)).toBe(expected);
    }
  );
});

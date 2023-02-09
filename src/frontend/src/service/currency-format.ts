export default function currencyFormat(input: number) {
  const isNegative = input < 0;
  const absValue = Math.abs(input);
  const wholePart = Math.trunc(absValue);
  const wholeStr = wholePart.toLocaleString();
  const fractionPart = absValue % 1;
  const fractionStr = fractionPart.toFixed(2).substring(1);
  const currencyString =
    "$" +
    (isNegative ? "(" : "") +
    wholeStr +
    fractionStr +
    (isNegative ? ")" : "");
  return currencyString;
}

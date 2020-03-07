export default function currencyFormat(input: number) {
  const wholePart = Math.trunc(input);
  const wholeStr = wholePart.toLocaleString();
  const fractionPart = Math.abs(input) % 1;
  const fractionStr = fractionPart.toFixed(2).substring(1);
  const currencyString = '$' + wholeStr + fractionStr;
  return currencyString;
}

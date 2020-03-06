export default function currencyFormat(input: number) {
  var wholePart = Math.trunc(input);
  var wholeStr = wholePart.toLocaleString();
  var fractionPart = Math.abs(input) % 1;
  var fractionStr = fractionPart.toFixed(2).substring(1);
  var rt = '$' + wholeStr + fractionStr;
  return rt;
}

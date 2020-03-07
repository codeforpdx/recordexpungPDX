import currencyFormat from './currency-format.ts';
describe('CURRENCY FORMAT SERVICE TEST', () => {
  it('formats currency', () => {
    var currencyString = currencyFormat(145);
    expect(currencyString).toEqual('$145.00');
    currencyString = currencyFormat(1231.45);
    expect(currencyString).toEqual('$1,231.45');
    currencyString = currencyFormat(0);
    expect(currencyString).toEqual('$0.00');
    currencyString = currencyFormat(-422.42);
    expect(currencyString).toEqual('$-422.42');
  });
});

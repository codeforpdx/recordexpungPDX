import currencyFormat from './currency-format.ts';
describe('CURRENCY FORMAT SERVICE TEST', () => {
  it('formats currency', () => {
    var str = currencyFormat(145);
    expect(str).toEqual('$145.00');
    str = currencyFormat(1231.45);
    expect(str).toEqual('$1,231.45');
    str = currencyFormat(0);
    expect(str).toEqual('$0.00');
    str = currencyFormat(-422.42);
    expect(str).toEqual('$-422.42');
  });
});

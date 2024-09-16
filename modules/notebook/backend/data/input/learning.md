### funding rate
- average premium index = (future - spot) / spot
  - different exchanges using different averaging methods
  - binance uses time average method
  - averaging the last 8 hours (???) using a time-weighted method
    - average_premium_index = (1 * premium_index_1 + 2 * premium_index_2 + ...)
- is calculated once every 5 seconds
- n = 60 / 5 + 60 * 8 = 5760
- premium index = ... (uses price differences)
  - premium index = max(0, bid - price index) - max(0, price index - ask)
  - only nonzero if outside of bid-ask spread
- interest free - you are borrowing usdt - you pay 1 bip every 8 hours
- annualized 20-30% returns if you let people borrow your usdt
- bonds of > regular bonds, credit default swap
- infinite funding rate - future price = spot price
- future difference arb on binance and bitget

### ???

### example: if it moves below bid then why do I want to make it higher?

### run research on server

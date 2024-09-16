### Consistency between backtest and demo trading

# Env: Current State
- trades are not profitable for some reason on live trading
- but is definitely profitable on back-testing
- we are using data from binance to backtest and testing on bybit
  - this shouldn't be an issue however

### The medium tester runs a successful backtest
- `data` has a `_data` field that first organizes by column name
  - `['open', 'close', 'high', 'low', 'taker_buy_quote_volume', 'quote_volume']`
  - then in each column name is a dataframe with columns are pair names
- then in `set_open_long` and ``

### Bybit

# Env: Ideal State
- live trading matches that of backtesting

# Env: Tactics
### Approach A: live trade for a while uninterrupted, then compare
- EdW has run live trading for a week
- can check if the backtest trader also makes the same trades as EDW
- this is like automod diff for preschoolers

### Approach B: backtest at the trade level on data

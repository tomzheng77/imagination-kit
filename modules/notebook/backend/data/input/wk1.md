# barter system
- https://github.com/barter-rs/barter-rs
- https://docs.rs/barter/latest/barter/

### what is the main architecture of barter?

### basic tutorial

### trader instance - only a single market pair?

### superconnected instance
- barter thing that connects to everything
- connects to three exchanges
- one of them being binance
- coerces other prices towards binance as it is faster

### side: snapshots
- log absolutely everything

### how does it set signal values?

### trade to candle event converter
* how often do we plugin in candles

### how many signal loops are there?
- if you speak into the tx, it then comes out of the rx
- command signal loop - this can be used to stop the engine
  - it is received only in the engine.run loop
- trader signal loop - same set of signals as the engine
  - the engine can propagate this down to traders
- trader event loop - communicates all events seen by the trader
- data event loop `self.data.next()`
  - sends `Feed::Next`, `Feed::Unhealthy` and `Feed::Finished`

### what components does the trader depend on?
- `Strategy` converts `MarketEvent` to `Signal`
  - it can have past state

### what does opening a trade end to end look like?
- the trader receives new market feed (`Feed::Next`) from its data
- this is used to generate a signal using `self.strategy.generate_signal`
- `portfolio.lock().generate_order` is used to generate an order (`Event::OrderNew`) from the signal
- the `Event::OrderNew` is used by `self.execution.generate_fill(&order)` to make a fill signal
- `portfolio.lock().update_from_fill(&fill)` produces side effects from the fill that can be any event
  - the `update_from_fill` calls `InMemoryRepository.set_open_position`
  - these side effects are logged into the `event_tx` but not fed back into the `event_q`

### how can one implement margin call?

### where does the table summary pull from?
- `self.portfolio.lock().get_statistics(&market_id)`
  - relies on `set_statistics` being called beforehand
    - which is called only if a trade is completed

### which part handles the delay from creating the order to it being filled?

### why are there two instances of `SimulatedExecution`?

### how does `barter` interact with `barter-execution`?

### how are close events handled?
- `parse_signal_decisions`

### why are there seemingly no trades by the example script?

### what keeps track of the open positions?

### how should I keep information that depends on past data?

### how do I backtest on past data?
- generate lots of signals based on past DB
- use trade signals to stimulate the engine


# env
- ability to
- 

### option 1: use conway but add fee etc
- pros
  - already have logic for futures on candle data
  - can add trade-based relatively quickly (2d)

### option 2: update simulate exchange logic
- easy of plugging into live system because same backtest/live

# env: implementing the execution framework in barter

# env: ability to execute trades across binance, bybit and biget
- would need L1 orderbook for 
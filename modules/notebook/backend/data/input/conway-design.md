# Project Conway: Simulator

### Components
- util-lib: contains the data loader, which can
- postgres - atomicity - can change to clickhouse at any time

### Next Steps
- ingest data from SQL DB

### Concepts
- spot
- perpetual futures
- delivery futures

### Crates
- data-fetcher and ??? should depend on util-lib

### Followups
- change util-lib::Market to util-lib::market
- replace `Data.load` timestamps with milliseconds since epoch
  - currently is "2024-05-07 11:08:16.580 +1000"
- rename the database tables such that it is not just SPOT
- python wrappers around `Trigger`

### Class: Data Loader
- can load K-line, trades or orderbook
- semantically, trades is equivalent to orderbook w/ depth 0

### Interface: Data
- name implies can load data for a market & can respond to queries with dataframes

### Concept: Strategy State Machine
- starts from IDLE
- then moves to PENDING_OPEN
- then HOLD
- and then PENDING_CLOSE
- finally IDLE again

### Concept: Strategy Signal
- LONG (token0, short token1) if `TBR(0) - TBR(1) < -0.1`
- SHORT (token0, long token1) if `TBR(0) - TBR(1) > 0.1`
- CLOSE (token0, close token1) if `|TBR(0) - TBR(1)| < 0.05`
- NULL otherwise

### Concept: `fill_bids_at_price` returns a tuple TODO

### Idea: `Strategy.prepare`
- this can augment the market's data frame with additional columns
  - which avoids additional complexity when calculating rolling values

### Requirement: Ability to Short TODO
- both long & short will be on the future (perpetuals) market

### Idea: Artificial Spread when Adding Orders

### Decision: If something is in OB should it still be in balance? TODO
- currently don't implement freezing amounts in orderbook
- still have cancel return the amount that would've been returned
  - (but now be careful not to get extra money from this)

### Interface: Market
- market is an interface that extends data
- should provide similar if not the same operation by actual exchanges
- we wouldn't treat a market as both OLHC and TradeFlow at the same time
  - if you register a K-line (OLHC) market for btcusdt
    - you would't register a TradeFlow-based market for the same pair

### Concept: Executor
- an executor knows how much you currently have (wallet)
- it has a list of markets
- its run function will keep repeating
  - advance markets
  - run strategy with markets
- advance should only advance the markets whose timestamps are the latest
- so then strategy can react to main data update of any market

### Implementations: TradeFlow, OLHC
- these implement `Market` and by extension `Data`
- each of these can also have a `depth` under `MarketData`

### Requirements
- can ingest different types of data from multiple markets
- executor executes a strategy
- strategy can have a python wrapper - then wrapper can run
- under the current market conditions

### Next Steps
- implement the following user flows
  - ingest data from SQL DB, run trading strategy

### PSQL Design on DB
```mermaid
```

### Data Hygeine

### Table Headings
#### trade_flow
- receive_ts, price, quantity, is_buyer_maker
  - NOTE: price, quantity are text
#### depth
- timestamp
#### olhc

### Ability to Debug
- each `Market` implementation should be able to print
- what type of market it is
- how much depth is loaded inside it
- and if verbose, a sample of its data & its depth

### Issue Log
- Cannot start a runtime from within a runtime.
  - cannot use postgres::Client in a tokio async

### Rust Knowledge
- tokio_postgres is async, postgres::Client is sync

### Local DB Setup
- table name convention
  - binance_spot_trade_usdteth
  - binance_ethusdt_depth_snapshots_level_10
- db_name: cex
- user: testuser
- pass: testuser
- tables:
  - binance_spot_trade_btcusdt
  - binance_spot_trade_ethusdt
  - btcusdt_order_book_snapshots_level_10
    - note: needs rename
  - ethusdt_order_book_snapshots_level_10
- alternative user: hfmm:new_password
- alternative user: thetadelta:new_password
- `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hfmm;`
- `ALTER TABLE ethusdt_order_book_snapshots_level_10 RENAME TO binance_ethusdt_depth_snapshots_level_10;`
- `ALTER TABLE btcusdt_order_book_snapshots_level_10 RENAME TO binance_btcusdt_depth_snapshots_level_10;`

### Postgres Concepts

### Small Decisions
- trigger takes in box, since we may want dynamic dispatch (TODO)
- bitget bybit perpetuals

# Envelope: Completing Conway V1

### Next Steps
- loading OLHC from the database
- completing the orderbook
  - except for `fill_at_price` everything is implemented
- completing the OLHC market
- (optional) completing the trade flow market
- completing the executor
- completing the tbr_pair strategy
- completing the backtester which calls the executor

### Grant User Access to All SQL Tables

### Semantics of `fill_at_price` TODO
- this should fill the top order by the amount

### Semantics of Market Advance
- the return value indicates if it has been advanced to a valid index
- need to understand
  - if get_markets returns 6 markets at timestamp `1337`
    - wouldn't advancing it produce 6 new markets at different timestamps
    - but is using `next_ts`
- move to the next index (simple)
- now I see the `open`, `low`, `high`, `close`
  - & I can fill in any bid order with `bid.price` < `low`
  - & I can fill in any ask order with `ask.price` > `high`
- this needs to update a balance, which needs to be a mut share

### prepare and advance
- prepare needs to add a rolling sum to the current dataframe
  - how does it do this?

### mut borrow more than once
```
fn open(&mut self, executor: &mut Executor) -> Result<(), Box<dyn Error>> {
    let market0 = executor.market_mut(&self.quote_token0, &self.base_token);
    let market1 = executor.market_mut(&self.quote_token1, &self.base_token);
    // ...
}
```

### TODO: how to ignore negative balance???


### TODO: negative stock fee calculation


### TODO: what kind of order gets rid of an ETH short?


### Was the python logic valid? TODO
- why is there an update close orders?

### Need to Work on List of Markets in Strategy TODO
- TODO: does it just need to know that the returned markets live long enough?

### How does it get data from the market?

### Rust Dataframe Access
- how do I access a specific column
- `df.column("col_name").f64().unwrap().get(2)`

### `the trait `market::Market` cannot be made into an object` TODO

### Why Is Taker Buyer Significant
- if the taker is a buyer
  - then asks should be updated, and bids cannot be matched

### Out of Scopes
- implementing alternative data sources such as depth, weather
- locking balance in the orderbook
- loading from the postgres DB with proper timestamps instead of string substituted into SQL
- implementing trade flow
- checking if "timestamptz" is handled correctly if treated as u64
- performance optimizations

### Should Market Exhausted Look Different?
- should it also be index = null or something else?

### Completing the Orderbook
- insert both bid and ask orders by the right order
- need to ensure somehow prints are done
- to my understanding the orderbook is complete & can be assumed correct

### Does `binary_search_by` fail if index is wrong?

### Rust: how to print debug

### Market Delegates to OrderBook

### Market Iteration

### Loading Market Data

# Envelope: Conway for Future Market
- position is different from ???
  - can be represented by a different (contract) balance
  - realized vs unrealized P&L

# Appendixes

### Appendix A: Print Debug
```
pub fn to_string(&self) -> String {
    // print a nice looking table of orders
    let mut buffer = String::new();
    if self.side == OrderSide::Ask {
        buffer.push_str(&format!("| {0: <59} |\n", "Ask Book"));
    } else {
        buffer.push_str(&format!("| {0: <59} |\n", "Bid Book"));
    }
    buffer.push_str(&format!("| {0: <10} | {1: <10} | {2: <10} | {3: <20} |\n", "Price", "Quantity", "Matched", "Timestamp"));
    let iter: Box<dyn Iterator<Item = &Order>> = if self.side == OrderSide::Bid {
        Box::new(self.orders.iter())
    } else {
        Box::new(self.orders.iter().rev())
    };
    for order in iter {
        let datetime: DateTime<Utc> = order.timestamp.into();
        let datetime_string = datetime.format("%Y-%m-%d %H:%M:%S").to_string();
        buffer.push_str(&format!("| {0: <10} | {1: <10} | {2: <10} | {3: <20} |\n", order.price, order.quantity, order.matched_quantity, datetime_string));
    }
    buffer
}


pub fn to_string(&self) -> String {
    let mut buffer = String::new();
    buffer.push_str(&self.asks.to_string());
    buffer.push_str(&self.bids.to_string());
    buffer
}
```

### Appendix B:
```
shape: (525_601, 5)
┌───────────────┬───────┬───────┬───────┬───────┐
│ ts            ┆ open  ┆ low   ┆ high  ┆ close │
│ ---           ┆ ---   ┆ ---   ┆ ---   ┆ ---   │
│ i64           ┆ f64   ┆ f64   ┆ f64   ┆ f64   │
╞═══════════════╪═══════╪═══════╪═══════╪═══════╡
```
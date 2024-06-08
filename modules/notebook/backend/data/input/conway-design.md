# Project Conway: Simulator

### Components
- util-lib: contains the data loader, which can
- postgres - atomicity - can change to clickhouse at any time

### Concepts
- spot
- perpetual futures
- delivery futures

### Next Steps
- ingest data from SQL DB

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
- `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hfmm;`
- `ALTER TABLE ethusdt_order_book_snapshots_level_10 RENAME TO binance_ethusdt_depth_snapshots_level_10;`
- `ALTER TABLE btcusdt_order_book_snapshots_level_10 RENAME TO binance_btcusdt_depth_snapshots_level_10;`

### Postgres Concepts

### Small Decisions
- trigger takes in box, since we may want dynamic dispatch (TODO)


- bitget bybit perpetuals


### Current State

# Env: P1
- is it possible to combine potree chunks with our own indexing structure
- in theory, assuming that laz supports ???
- instead of implementing from scratch why not use the existing software?
- let potree generator do its thing, we then use the output
- `PointCloudSelection` is made lazy. things which consume it
  - for now lazy subclass called `LazyPointCloudSelection`
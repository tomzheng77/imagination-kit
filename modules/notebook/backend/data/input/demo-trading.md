### 30 USD button
- on every 30 USD click the close button
  - idea is to rely on one signal, not two
- if a signal is valid on time T, it surely will degrade as time goes on

# Understanding the States
- `mint` is called on the function per trader
- as soon as an open order is placed, you get an order ID
- parse_order_response -> [0]
  - ('1419f82e-4cee-4690-a0f7-5ad2359dfe0c', 'OK')
- if order null and pending open, why become in position?

### Does amend change the order ID?

# Understanding the Existing Strategy

### What is the signal?
- on each tick there is a signal
- over-sell if TBR < 0.35
  - meaning less than 35% of the volume in the last X minutes are buyers
- over-buy if TBR > 0.65

### What are the states
- initially it is `IDLE` as there are no positions & no orders
- if a signal is received that is OVER_SELL
  - it will open a maker order that is BID
    - opening positions are HTTP calls, so are "instant"
  - it then stays in `PENDING_OPEN`
- if state is `PENDING_OPEN` and there are no orders
  - we can assume the order has been fully executed
  - the state is then changed to `HOLD`
- if the state is `HOLD` and the opposite signal is received
  - then we should try to close the position
  - it should start a market order which again, is instant
  - the order then presumably stays and we are in `PENDING_CLOSE`
- if the state is `PENDING_CLOSE` and there ar eno orders
  - the order has been executed and now we are in `IDLE`

# Improving the Existing Strategy

### Continuous Closing
- if in `PENDING_CLOSE` and the order still hasn't been closed for 10 minutes

### Instant Exit
- if the SIGTERM (not SIGKILL) signal has been received by the program
  - and it is currently in the `HOLD` state
    - it should change to `PENDING_CLOSE`
  - and in the `PENDING_CLOSE` state
    - (it will as-is now continuously create close orders)
    - (currently it will poll at 1min intervals)
  - and only allow it to exit if it naturally came to `IDLE`

# Matching the Backtest Output
- need to check how backtesting is currently conducted

### Log All Orders
- need to log all orders such that it can be matched against order history
- every time an order is opened
  - when an open signal is received
    - when an open order has not been hit and should be cancelled
  - when a close signal is received
    - when a close order has not been hit and should be restarted
      - the ID of the new order should also be logged
- the ID, type, price and quantity & reason of the order should be logged

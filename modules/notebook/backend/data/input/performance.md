### 500ms for empty run on 1M rows
- 0.5us per trade

### 8.5s for initial
- 8.5us per trade

### 4.3s for mut reference
- 4.3us per trade

### receive event order issue
- first short position was opened, then order was filled, then order was cancelled
- why keep losing money ?
- only after the dust clears to account events get through
- where does the third BalanceUpdate come from?
```
Before run_backtester
Open short position Some(1450) Some(1500.0) Some(1600.0)
sending event for order update
Cancel order due to signal reversal Some(550) Some(400.0) Some(500.0)
Open long position Some(550.010) Some(400.0) Some(500.0)
sending event for order update
Account event OrderUpdate(OrderUpdateData { order_id: 0, client_id: 40e0ad2a-e0f8-48eb-921d-830191ad4f7d, quantity: 2.0, filled_quantity: 2.0 })
Account event BalanceUpdate(BalanceUpdateData { token: Token { name: String16 { buffer: "Tether" }, symbol: String16 { buffer: "USDT" }, decimals: 6 }, delta: -2.9000 })
Account event OrderUpdate(OrderUpdateData { order_id: 1, client_id: 40e0ad2a-e0f8-48eb-921d-830191ad4f7d, quantity: 2.0, filled_quantity: 2.0 })
Account event BalanceUpdate(BalanceUpdateData { token: Token { name: String16 { buffer: "Tether" }, symbol: String16 { buffer: "USDT" }, decimals: 6 }, delta: -1.1000200 })
Account event BalanceUpdate(BalanceUpdateData { token: Token { name: String16 { buffer: "Tether" }, symbol: String16 { buffer: "USDT" }, decimals: 6 }, delta: -1799.9800 })
Finished sending events
Terminating strategy, total event count: 400006
```

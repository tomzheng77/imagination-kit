# Env run geth
- https://geth.ethereum.org/docs/getting-started
- https://lighthouse-book.sigmaprime.io/run_a_node.html
- https://eth-clients.github.io/checkpoint-sync-endpoints/
- https://lighthouse-book.sigmaprime.io/faq.html
- https://github.com/ethereum/go-ethereum/issues/25911

### Geth depends on consensus client
"Geth will not sync the blockchain correctly unless there is also a consensus client that can pass Geth a valid head to sync up to.
In a separate terminal, start a consensus client.
Once the consensus client gets in sync, Geth will start to sync too."

### Initial Attempt
- `geth --syncmode "full" --http --http.addr 0.0.0.0 --http.vhosts="*" --http.corsdomain="*" --datadir geth-rundir`
- `lighthouse bn --datadir lighthouse-rundir --http --execution-endpoint http://127.0.0.1:8551 --jwt-secrets geth-rundir/geth/jwtsecret --checkpoint-sync-url=https://sync-mainnet.beaconcha.in`

### LH Sepolia
- `clef newaccount --keystore geth-tutorial/keystore`
- `clef --keystore geth-tutorial/keystore --configdir geth-tutorial/clef --chainid 11155111`
- `geth --sepolia --datadir geth-tutorial --authrpc.addr localhost --authrpc.port 8551 --authrpc.vhosts localhost --authrpc.jwtsecret geth-tutorial/jwtsecret --http --http.api eth,net --signer=geth-tutorial/clef/clef.ipc --http`
- `lighthouse bn --network sepolia --datadir lighthouse-tutorial --http --execution-endpoint http://127.0.0.1:8551 --jwt-secrets geth-tutorial/jwtsecret --checkpoint-sync-url=https://checkpoint-sync.holesky.ethpandaops.io`

### Prysm Tutorial
- https://docs.prylabs.network/docs/install/install-with-script
- `./prysm.sh beacon-chain --execution-endpoint=http://localhost:8551 --mainnet --jwt-secret=../jwt.hex --checkpoint-sync-url=https://beaconstate.info --genesis-beacon-api-url=https://beaconstate.info --datadir=data-dir`


### Erigon
- https://github.com/ledgerwatch/erigon
- `erigon --datadir=erigon-mainnet --chain=mainnet --port=30303 --http.port=8545 --authrpc.port=8551 --torrent.port=42069 --private.api.addr=127.0.0.1:9090 --http --ws --http.api=eth,debug,net,trace,web3,erig --internalcl`
```
chaindata: recent blocks, state, recent state history. low-latency disk recommended.
snapshots: old blocks, old state history. can symlink/mount it to cheaper disk. mostly immutable. must have ~100gb free space (for merge recent files to bigger one).
temp: can grow to ~100gb, but usually empty. can symlink/mount it to cheaper disk.
txpool: pending transactions. safe to remove.
nodes: p2p peers. safe to remove.
```

### Datadir vs Ancient
- `geth --http --http.api personal,eth,net,web3 --datadir C:\ETH\Node --datadir.ancient F:\ETH\Node\geth\chaindata\ancient`

### EthersJS
- https://magnushansson.xyz/blog_posts/crypto_defi/2021-12-27-Run-Erigon-Archive-Node
```
// Comment in console
console.log("Starting!");

// Import libraries
import { ethers } from "ethers";

// Set provider (Ethereum node)
const provider = new ethers.providers.WebSocketProvider('ws://127.0.0.1:8545');

// Set transaction
const tx_hash = '0x5e1657ef0e9be9bc72efefe59a2528d0d730d478cfc9e6cdd09af9f997bb3ef4';

// Define function to retrive tx
async function localTx() {
    const tx = await provider.getTransaction(tx_hash)
    const receipt = await provider.getTransactionReceipt(tx_hash)
    console.log(tx)
    console.log(receipt)
    console.log('Complete!')
};

// Export main function
export const run = () => {
  localTx().catch(err => console.error(err));
};
```

### GetBlockReceipts
- https://docs.chainstack.com/docs/uncovering-the-power-of-ethgetblockreceipts

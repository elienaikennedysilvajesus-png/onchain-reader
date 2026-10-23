# onchain-reader

A small Python tool that reads **live on-chain data** from an ERC-20 token on
the [Base](https://base.org) network using [web3.py](https://web3py.readthedocs.io).

It connects to Base over a public RPC (no API key needed), loads a token
contract, and prints its name, symbol, decimals, total supply, and the balance
of any address.

## Why

A clean, self-contained example that I can:

- connect to an EVM chain,
- read a smart contract's state,
- and handle token decimals correctly (the step most people get wrong).

## Run

> Use Python 3.11–3.13. web3.py does not yet ship wheels for 3.15.

```bash
pip install -r requirements.txt

# Reads USDC on Base by default:
python read_token.py

# Or pass any ERC-20 token and holder address:
python read_token.py 0xToken... 0xHolder...
```

## Example output

```
Network      : Base (chain id 8453), block 53,001,816
Token        : USD Coin (USDC)
Address      : 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
Decimals     : 6
Total supply : 4,289,981,452.1076 USDC
Holder       : 0x3304E22DDaa22bCdC5fCa2269b418046aE7b566A
Balance      : 79,709.1050 USDC
```

(The exact numbers change every block — this is real, current data.)

## How it works

1. Connect to Base via `Web3.HTTPProvider`.
2. Build a contract object from the token address and a minimal ERC-20 ABI.
3. Call the read-only functions (`name`, `symbol`, `decimals`, `totalSupply`,
   `balanceOf`) — these cost no gas.
4. Convert raw integer amounts to human-readable values by dividing by
   `10 ** decimals`.

## Tech

Python · web3.py · Base (EVM)

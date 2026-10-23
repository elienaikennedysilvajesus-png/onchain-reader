"""
onchain-reader — read live on-chain data from an ERC-20 token on Base.

What it does:
  Connects to the Base network over a public RPC (no API key needed),
  loads an ERC-20 token contract, and prints its name, symbol, decimals,
  total supply, and the balance of any address you pass in.

Why it exists:
  A small, self-contained proof that I can connect to an EVM chain,
  read a smart contract, and handle token decimals correctly with web3.py.

Usage:
  python read_token.py                 # reads USDC on Base (default)
  python read_token.py <token> <holder>

Requires: web3 (see requirements.txt). Tested with web3 >= 6.0.
"""

import sys
from web3 import Web3

# Public Base mainnet RPC. No key required, good enough for reads.
BASE_RPC = "https://mainnet.base.org"

# Defaults: USDC on Base, and the Base USDC bridge as a sample holder.
DEFAULT_TOKEN = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"   # USDC (Base)
DEFAULT_HOLDER = "0x3304E22DDaa22bCdC5fCa2269b418046aE7b566A"  # sample address

# Minimal ERC-20 ABI: only the read functions we call.
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "name",
     "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol",
     "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals",
     "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply",
     "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
     "type": "function"},
]


def human(amount_raw: int, decimals: int) -> str:
    """Turn a raw on-chain integer into a human-readable number.

    On-chain, token amounts are integers with no decimal point. A token with
    18 decimals stores 1 token as 1_000_000_000_000_000_000. We divide by
    10**decimals to get the real value. Getting this wrong is the most common
    beginner bug, so it lives in its own function.
    """
    return f"{amount_raw / (10 ** decimals):,.4f}"


def main() -> None:
    # Allow overriding token and holder from the command line.
    token = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TOKEN
    holder = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_HOLDER

    # Connect to the chain.
    w3 = Web3(Web3.HTTPProvider(BASE_RPC))
    if not w3.is_connected():
        sys.exit("Could not connect to Base RPC. Try again in a moment.")

    # Checksum the addresses (web3 requires the mixed-case form).
    token = Web3.to_checksum_address(token)
    holder = Web3.to_checksum_address(holder)

    # Build the contract object and call its read-only functions.
    contract = w3.eth.contract(address=token, abi=ERC20_ABI)
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply = contract.functions.totalSupply().call()
    balance = contract.functions.balanceOf(holder).call()

    # Report.
    block = w3.eth.block_number
    print(f"Network      : Base (chain id {w3.eth.chain_id}), block {block:,}")
    print(f"Token        : {name} ({symbol})")
    print(f"Address      : {token}")
    print(f"Decimals     : {decimals}")
    print(f"Total supply : {human(total_supply, decimals)} {symbol}")
    print(f"Holder       : {holder}")
    print(f"Balance      : {human(balance, decimals)} {symbol}")


if __name__ == "__main__":
    main()

import csv
import json
import argparse
from web3 import Web3


class GetETHInfo:
    def __init__(self, address, rpc_url):
        self.address = address

        # RPC Url configuration
        rpc_url = "fill-rpc-url-here"

        # Web3 ETH client
        self.web3 = Web3(provider=Web3.HTTPProvider(rpc_url))

        # Price feed
        with open("./abis/aggregator_abi.json", "r") as f:
            price_feed_abi = json.load(f)

        # Mainnet eth/usd chainlink pricefeed
        price_feed_address = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
        self.price_feed = self.web3.eth.contract(
            address=price_feed_address, abi=price_feed_abi
        )

        # Supported ERC-20 token addresses
        with open("abis/erc20_abi.json", "r") as f:
            self.erc20_abi = json.load(f)
        self.erc20_addresses = {"tehter": "0xdAC17F958D2ee523a2206206994597C13D831ec7"}

    def balance(self) -> float:
        balance = self.web3.eth.get_balance(self.address)
        return float(self.web3.from_wei(balance, "ether"))

    def usd_balance(self) -> float:
        ether = self.balance()
        usd_price = (
            self.price_feed.functions.latestRoundData().call()[1] / 1e8
        )  # Latest price in USD/ETH
        usd_amount = ether * usd_price
        return usd_amount

    def erc20_contract(self, contract_address):
        return self.web3.eth.contract(address=contract_address, abi=self.erc20_abi)

    def erc20_holdings(self):
        holdings = {}
        for token, contract_address in self.erc20_addresses.items():
            token_contract = self.erc20_contract(contract_address)
            balance = token_contract.functions.balanceOf(self.address).call()
            holdings[token] = balance
        return holdings

    def erc20_output(self):
        contract = self.erc20_contract(self.address)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        owner = contract.functions.owner().call()
        total_supply = contract.functions.totalSupply().call()

        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Name", "Symbol", "Address", "Owner", "Total Supply", "Decimals"]
            )
            writer.writerow([name, symbol, self.address, owner, total_supply, decimals])

    def wallet_output(self):
        balance_ = getInfo.balance()
        usd_ = getInfo.usd_balance()
        erc20_: dict = getInfo.erc20_holdings()

        header = ["Address", "Balance", "USD"] + [f"{k}_holding" for k in erc20_]
        row = [self.address, balance_, usd_] + list(erc20_.values())
        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("address", help="ETH crypto address", type=str)
    parser.add_argument(
        "--erc20", action="store_true", help="Define as ERC20 token contract address"
    )
    args = parser.parse_args()

    getInfo = GetETHInfo(address=args.address)
    if args.erc20:
        getInfo.erc20_output()
    else:
        getInfo.wallet_output()

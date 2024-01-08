
# ETH Information Fetcher  
   
This is a simple script that fetches and exports Ethereum address information, including balance, USD balance, and ERC20 holdings, to a CSV file. It also fetches and exports ERC20 token metadata when given an ERC20 token contract address.  
   
## Setup  
   
1. Install the required packages with pip (requirements.txt)     
2. Replace `fill-rpc-url-here` with your Ethereum Mainnet RPC url in the `GetETHInfo` class constructor:  
   
## Usage  
   
Ethereum address wallet information export usage:  
   
```bash  
python main.py 0x63A395B574D5E23C3dbC6986Be5994Ef6743aFA8  
```  
   
ERC20 token contract address metadata export usage:
   
```bash  
python main.py 0xdAC17F958D2ee523a2206206994597C13D831ec7 --erc20  
```  
   
Create a CSV file named `output.csv`

   
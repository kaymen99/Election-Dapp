
## Election-Dapp



## Overview:

A Decentralized Voting Application built for EVM compatible blockchains (ethereum, polygon, avalanche,...), it has the following features :

<h3>Administation functions: </h3>
<ul>
  <li>Adding new candidates</li>
  <li>Opening the voting for a giver duration </li>
  <li>Closing the election after the predermined voting period </li>
</ul>

<h3>Main functions: </h3>
<ul>
  <li>Allow user to vote only once for a choosen candidate</li>
  <li>Determine the winner based on highest votes count </li>
  <li>Give a complete list of all candidates with their data (id, name, votes count) </li>
</ul>


### Installation & Setup:

1. Installing Brownie: Brownie is a python framework for smart contracts development,testing and deployments. It's quit like [HardHat](https://hardhat.org) but it uses python for writing test and deployements scripts instead of javascript.
   Here is a simple way to install brownie.
   ```sh
    pip install --user pipx
    pipx ensurepath
    # restart your terminal
    pipx install eth-brownie
   ```
   Or if you can't get pipx to work, via pip (it's recommended to use pipx)
    ```sh
    pip install eth-brownie
    ```
   
2. Clone the repo:
   ```sh
   git clone https://github.com/Aymen1001/Election-Dapp.git
   cd Election-Dapp
   ```

### Testing:

The tests for the Election smart contract can be found in the tests folder, you can run all the tests by :
   ```sh
   brownie test
   ```
Or you can test each function individualy:
   ```sh
   brownie test -k <function name>
   ```

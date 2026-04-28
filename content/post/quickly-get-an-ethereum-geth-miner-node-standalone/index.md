---
title: "Quickly get an Ethereum Geth miner node standalone"
date: 2017-06-02T16:59:17+0000
lastmod: 2017-06-02T16:59:17+0000
slug: "quickly-get-an-ethereum-geth-miner-node-standalone"
feature_image: "https://www.cicoria.com/content/images/2017/06/sean-dubois-5753-compressed.jpg"
aliases:
  - /quickly-get-an-ethereum-geth-miner-node-standalone/
---

I know there are other scripts, etc. out there. But I can't seem to find them when I need them.

So, I created a GitHub repo that contains a set of scripts and simple steps that will download Geth, initialize the chain, then run a miner locally with the RPC endpoints open so you can develop quickly.

The bits are here: <https://github.com/EthereumEx/standalone-miner>

Of the shell scripts, initialization is of most interest. What it does is generate a new account with a blank passphrase, then trims the account public address from the output and uses that in the genesis.json file. The same address is then used for the miner's etherbase address - the address that gets mining credit.

```
#!/usr/bin/env bash
set -x

rm -rf passphrase.txt ./data

echo "" > passphrase.txt

ADDRESS=$(./geth --datadir ./data account new --password passphrase.txt | cut -f 2 -d ' '| cut -c 2-41)

echo $ADDRESS > address.txt

sed  "s/address1/${ADDRESS}/" genesis.template.json > genesis.json

./geth --datadir ./data init ./genesis.json

```

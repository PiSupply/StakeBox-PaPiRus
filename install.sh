#!/usr/bin/env bash

sudo apt-get update

sudo apt-get install python-pip git bc i2c-tools fonts-freefont-ttf whiptail make gcc -y

pip install python-bitcoinrpc

git clone https://github.com/ChristopherRush/stakebox-papirus.git

RPCPASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

neblioqt=/home/pi/Desktop/neblio-qt
reddcoinqt=/home/pi/reddcoin-2.0.1.2/reddcoin-qt

if [ -e "$neblioqt" ]; then
    echo "neblio installed....checking config file"
    neblio=/home/pi/.neblio/neblio.conf
    if [ -e "$neblio" ]; then
        echo "Config file already exists at $neblio"
    else
        echo "File does not exist"
        touch $neblio
        echo "neblio.conf file created"
        echo "rpcpassword=$RPCPASSWORD" >> $neblio
        echo "rpcuser=nebliorpc" >> $neblio
        echo "rpcport=8332" >> $neblio
        echo "rpcallowip=127.0.0.1" >> $neblio
        echo "configuration settings appended"
    fi
else
    echo "neblio not installed on this StakeBox"

fi

if [ -e "$reddcoinqt" ]; then
    echo "reddcoin installed....checking config file"
    reddcoin=/home/pi/.reddcoin/reddcoin.conf
    if [ -e "$reddcoin" ]; then
        echo "Config file already exists at $reddcoin"
    else
        echo "File does not exist"
        touch $reddcoin
        echo "reddcoin.conf file created"
        echo "rpcpassword=$RPCPASSWORD" >> $reddcoin
        echo "rpcuser=reddcoinrpc" >> $reddcoin
        echo "rpcport=8332" >> $reddcoin
        echo "rpcallowip=127.0.0.1" >> $reddcoin
        echo "configuration settings appended"
    fi
else
    echo "reddcoin not installed on this StakeBox"

fi

if [ -e "$qtumd" ]; then
    echo "qtum installed....checking config file"
    qtum=/home/pi/.qtum/qtum.conf
    if [ -e "$qtum" ]; then
        echo "Config file already exists at $qtum"
    else
        echo "File does not exist"
        touch $qtum
        echo "qtum.conf file created"
        echo "rpcpassword=$RPCPASSWORD" >> $qtum
        echo "rpcuser=qtumrpc" >> $qtum
        echo "rpcport=8332" >> $qtum
        echo "rpcallowip=127.0.0.1" >> $qtum
        echo "configuration settings appended"
    fi
else
    echo "qtum not installed on this StakeBox"

fi

if [ -e "$trezarqt" ]; then
    echo "TrezarCoin installed....checking config file"
    trezar=/home/pi/.trezarcoin/trezarcoin.conf
    if [ -e "$trezar" ]; then
        echo "Config file already exists at $trezar"
    else
        echo "File does not exist"
        touch $trezar
        echo "trezarcoin.conf file created"
        echo "rpcpassword=$RPCPASSWORD" >> $trezar
        echo "rpcuser=trezarcoinrpc" >> $trezar
        echo "rpcport=8332" >> $trezar
        echo "rpcallowip=127.0.0.1" >> $trezar
        echo "configuration settings appended"
    fi
else
    echo "TrezarCoin not installed on this StakeBox"

fi

git clone https://github.com/PiSupply/PaPiRus.git

cd PaPiRus

sudo bash install

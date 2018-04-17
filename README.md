# StakeBox PaPiRus Display
<p align="center">
  <img width="400" src="https://cdn.shopify.com/s/files/1/2685/8754/files/logo-wide_x200.png">
</p>

This project uses the PaPiRus 2.7" e-ink display to show all your StakeBox statistics such as network status, staking information as well as your current address and QR code for transferring coins/tokens to your wallet. This project is currently compatible with the following StakeBoxes:
- [Neblio](https://www.stakebox.org/collections/stakeboxes/products/neblio-stakebox)
- [QTUM](https://www.stakebox.org/collections/stakeboxes/products/qtum-stakebox)
- [Reddcoin](https://www.stakebox.org/collections/stakeboxes/products/reddcoin-stakebox)
- [Trezarcoin](https://www.stakebox.org/collections/stakeboxes/products/trezarcoin-stakebox)


## Hardware setup

You will need the following hardware to setup your StakeBox Display:

- [StakeBox](https://www.stakebox.org)
- [PaPiRus Display HAT](https://uk.pi-supply.com/products/papirus-epaper-eink-screen-hat-for-raspberry-pi)
- [PaPiRus HAT Case](https://uk.pi-supply.com/products/papirus-hat-case)

Currently this software is only compatible with the 2.7" e-ink display due to display size restrictions.

## Software

The display script is fully automated, in which it will automatically setup the configuration files for the RPC server to access and then parse them into our python script. It doesn't matter which version of the StakeBox you have as the program will locate the installation files for you and create the config file in that particular directory.


### Auto Installation

The auto installation script will install all the dependancies and project files as well as creating the configuration files for your staking application. Just run the following command in the terminal window making sure you have internet access on your StakeBox:

```bash
# Run this line and the weather station will be setup and installed
curl -sSL https://raw.githubusercontent.com/ChristopherRush/stakebox-papirus/master/install.sh | sudo bash
```

### Manual Installation

If you are having trouble with the auto installation script or you would like to manually install the project files and dependancies then you can follow these steps:

1. First of all make sure you have the latest version of OS running on your StakeBox with the following command:
```bash
sudo apt-get update
```
2. Install some dependancies required for both the StakeBox project as well as the PaPiRus display:
```bash
sudo apt-get install python-pip git bc i2c-tools fonts-freefont-ttf whiptail make gcc -y
```
3. In order for us to connect to the RPC server that the StakeBox application is running we will need a python RPC client so we can connect issue commands to the server. For this we are going to use the Bitcoin RPC Python package, which has been specifically design for bitcoin style cryptocurrencies:
```bash
pip install python-bitcoinrpc
```
4. Download the StakeBox PaPiRus display project files:
```bash
git clone https://github.com/ChristopherRush/stakebox-papirus.git
```
5. In order for both the RPC server and the RPC client to connect to one another you will need to create a configuration file with all the server settings such as username and password. Run the following script from the StakeBox project file to create the config file if it is not already created:
```bash
bash config.sh
```
If the configuration file has already been created by the Staking application then you will need to amend the file with the following settings, where [password] is replaced with your own:
```config
rpcpassword=[password]
rpcuser=reddcoinrpc
rpcport=8332
rpcallowip=127.0.0.1
```
You can find the configuration file in the application directory:
- neblio - /home/pi/.neblio/neblio.config
- reddcoin - /home/pi/.reddcoin/reddcoin.conf
- qtum - /home/pi/.qtum/qtum.conf
- trezarcoin /home/pi/.trezarcoin/trezarcoin.conf

6. Finally you can install the PaPiRus library using the following instalation script or if you wish to install manually you can follow the steps on the PaPiRus [GitHub](https://github.com/PiSupply/PaPiRus) page:
```bash
curl -sSL https://pisupp.ly/papiruscode | sudo bash
```

## Usage

In order to run the Staking application with the RPC server you will need to launch it from the command line with the following command, depending on which StakeBox you have:
```bash
#neblio
cd /home/pi/Desktop
./neblio-qt -server

#Reddcoin
cd /home/pi/reddcoin-2.0.1.2
./reddcoin-qt -server

#QTUM
qtumd daemon

#TrezarCoin
cd /home/pi/Desktop
./trezarcoin-qt -server
```

NOTE: You cannot run this command using SSH, it must be run from the Desktop GUI

Once the Staking application is running on the Desktop you can then begin to start the StakeBox PaPiRus display program with the following command:
```bash
cd stakebox-papirus
sudo python stakebox-papirus.py
```

## Display features

The display will show 5 different screens based on the status of the staking application. When you first run the program it will show the StakeBox logo with the server status at the bottom:

- Down - the RPC server is not running
- Active - the RPC server is running

At this point you can select one of four buttons (from left to right) at the top of the display to show your staking information:

- System information (SW4)
  - Current Version
  - Balance
  - Stake
  - Connections
  - Blocks
  - Proof of Stake Difficulty
- Staking Information (SW3)
  - Staking Status
  - Current Block Size
  - Current Block Size Tx
  - Pooled Tx
  - Difficulty
  - Weight
  - Net Stake Weight
  - Expected Time
- Unknown (SW2)
- Staking address (SW1)
  - QR Code

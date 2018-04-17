#    Copyright (C) 2018  Christopher Rush
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import RPi.GPIO as GPIO
import sys
import ConfigParser #used to parse config file
import os
import StringIO
import urllib

from papirus import Papirus
from time import sleep
from papirus import PapirusImage
from papirus import PapirusComposite
from bitcoinrpc.authproxy import AuthServiceProxy
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()


WHITE = 1
BLACK = 0

CLOCK_FONT_FILE = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
DATE_FONT_FILE  = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'

nebliopath='/home/pi/.neblio/neblio.conf'
qtumpath='/home/pi/.qtum/qtum.conf'
reddcoinpath='/home/pi/.reddcoin/reddcoin.conf'
trezarcoinpath='/home/pi/.trezarcoin/trezarcoin.conf'

config_path = ""
server_status = False

#add while statement here
#Check with staking application is installed
if os.path.isfile(nebliopath):
    config_path = nebliopath
    print "Neblio installed"
else:
    print "Neblio not installed"

if os.path.isfile(reddcoinpath):
    config_path = reddcoinpath
    print "Reddcoin installed"
else:
    print "Reddcoin not installed"

if os.path.isfile(qtumpath):
    config_path = qtumpath

    print "QTUM installed"
else:
    print "QTUM not installed"

if os.path.isfile(trezarcoinpath):
    config_path = trezarcoinpath

    print "TrezarCoin installed"
else:
    print "TrezarCoin not installed"

if config_path == "":
    print "No configuration file found. Please run config.py to setup"
    sys.exit()


#Parse config file so you can read its values
with open(config_path, 'r') as f:
    a = '[config]\n' #Adds section header to the string. By default the staking app cannot read the config file if there is a section header
    b = f.read()
    config_string = a + b
buf = StringIO.StringIO(config_string) #Creates a buffer
config = ConfigParser.ConfigParser()
config.readfp(buf)

#Server RPC URL
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%((config.get('config','rpcuser')),(config.get('config','rpcpassword'))))
#print rpc_connection
#Get server status must run xxxx-qt -server first



try:
    getaddress = rpc_connection.getaccountaddress('')

    #QR Code URL from Google APi
    url ='http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=%s' %getaddress

    #Download QR code
    urllib.urlretrieve(url, '/home/pi/stakebox-papirus/images/qr.png')
    rpc_connection.getinfo()
    server_status = True
except:
    server_status = False
    pass

#Button GPIO pins
SW1 = 16
SW2 = 19
SW3 = 20
SW4 = 21

GPIO.setmode(GPIO.BCM) #Use BCM GPIO numbering

#Set GPIO pins as inputs
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)
GPIO.setup(SW3, GPIO.IN)
GPIO.setup(SW4, GPIO.IN)


papirus = Papirus() #create papirus object
textNImg = PapirusComposite(False) #create variable to store image/text

#Boot image when started
if server_status == True:
    textNImg.AddText("Press a button", 50, 5, Id="Start" )
    textNImg.AddImg("images/StakeBox-Black.bmp",69,25,(125,125), Id="BigImg")
    textNImg.AddText("Server Status: Active ", 10, 156, Id="bottom")
    textNImg.WriteAll()
else:
    textNImg.AddText("Press a button", 50, 5, Id="Start" )
    textNImg.AddImg("images/StakeBox-Black.bmp",69,25,(125,125), Id="BigImg")
    textNImg.AddText("Server Status: Down ", 10, 156, Id="bottom")
    textNImg.WriteAll()
    #Exit program if RPC server is not running
    sys.exit('server not running')


def main(argv):
        papirus = Papirus(rotation = int(argv[0]) if len(sys.argv) > 1 else 0)
        draw_image(papirus)


def draw_image(papirus):
     # initially set all white background
    image = Image.new('1', papirus.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    clock_font_size = int((width - 4)/(20*0.65))      # 18 chars HH:MM:SS
    clock_font = ImageFont.truetype(CLOCK_FONT_FILE, clock_font_size)

     # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    while True:

        if GPIO.input(SW1) == False:
            textNImg = PapirusComposite(False) #Clears the draw buffer
            textNImg.AddImg("images/qr.png",60,10,(150,150), Id="BigImg")
            textNImg.WriteAll()

        if GPIO.input(SW3) == False:
            papirus.clear()
            while GPIO.input(SW3) == True & GPIO.input(SW1) == True & GPIO.input(SW4) == True:
                #Get info from RPC connection
                if config_path == trezarcoinpath:
                    get_blocks = rpc_connection.getmininginfo()["blocks"]
                    get_difficulty = rpc_connection.getmininginfo()["posdifficulty"]

                    blocks = ('Blocks: %d' % get_blocks)
                    difficulty = ('POS Difficulty: %d' % get_difficulty)
                    get_curr_block_size = rpc_connection.getmininginfo()["currentblocksize"]
                    get_curr_block_tx = rpc_connection.getmininginfo()["currentblocktx"]
                    get_pooledtx = rpc_connection.getmininginfo()["pooledtx"]
                    get_netweight = rpc_connection.getmininginfo()["stakeweight"]

                else:
                    get_staking = rpc_connection.getstakinginfo()["staking"]
                    get_search = rpc_connection.getstakinginfo()["search-interval"]
                    get_weight = rpc_connection.getstakinginfo()["weight"]
                    get_exp_time = rpc_connection.getstakinginfo()["expectedtime"]

                    search_int = ('Search: %d' % get_search)
                    weight = ('Weight: %d' % get_weight)
                    staking = ('Staking: %s' % get_staking)
                    expectedtime = ('Expected: %f' % get_exp_time)

                get_curr_block_size = rpc_connection.getstakinginfo()["currentblocksize"]
                get_curr_block_tx = rpc_connection.getstakinginfo()["currentblocktx"]
                get_pooledtx = rpc_connection.getstakinginfo()["pooledtx"]
                get_netweight = rpc_connection.getstakinginfo()["stakeweight"]


                #Append value to string
                currentblocksize = ('Block Size: %d' % get_curr_block_size)
                currentblocktx = ('Block Tx: %d' % get_curr_block_tx)
                pooledtx = ('PooledTx: %d' % get_pooledtx)
                netweight = ('Net Weight: %d' % get_netweight)



                #Write to the PaPiRus screen
                draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)

                if config_path == trezarcoinpath:
                    draw.text((5, 10), blocks, fill=BLACK, font=clock_font)
                    draw.text((5, clock_font_size + 70), difficulty, fill=BLACK, font=clock_font)

                else:
                    draw.text((5, 10), staking, fill=BLACK, font=clock_font)
                    draw.text((5, clock_font_size + 70), search_int, fill=BLACK, font=clock_font)
                    draw.text((5, clock_font_size + 90), weight, fill=BLACK, font=clock_font)
                    draw.text((5, clock_font_size + 130), expectedtime, fill=BLACK, font=clock_font)

                draw.text((5, clock_font_size + 10), currentblocksize, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 30), currentblocktx, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 50), pooledtx, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 110), netweight, fill=BLACK, font=clock_font)



                papirus.display(image)

                papirus.partial_update()

        if GPIO.input(SW4) == False:
            papirus.clear()
            while GPIO.input(SW3) == True & GPIO.input(SW1) == True & GPIO.input(SW4) == True:

                get_version = rpc_connection.getinfo()["version"]
                get_balance = rpc_connection.getinfo()["balance"]
                get_stake = rpc_connection.getinfo()["stake"]
                get_connection = rpc_connection.getinfo()["connections"]
                get_blocks = rpc_connection.getinfo()["blocks"]
                if config_path == trezarcoinpath:
                    get_pos = rpc_connection.getmininginfo()["posdifficulty"]
                else:
                    get_pos = rpc_connection.getstakinginfo()["posdifficulty"]

                version = ('Version: %s' % get_version)
                balance = ('Balance: %f' % get_balance)
                stake = ('Stake: %f' % get_stake)
                connections = ('Connections: %d' % get_connection)
                blocks = ('Blocks: %d' % get_blocks)
                pos = ('PoS: %f' % get_pos)

                #Write to the PaPiRus screen
                draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
                draw.text((5, 10), version, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 10), balance, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 30), stake, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 50), connections, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 70), blocks, fill=BLACK, font=clock_font)
                draw.text((5, clock_font_size + 90), pos, fill=BLACK, font=clock_font)
                papirus.display(image)

                papirus.partial_update()
    sleep(0.1)

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

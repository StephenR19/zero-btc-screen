# --Forked Version Changes--

This version uses CoinGecko api specifically /coins/{id}/ohlc and it can cycle through a list of crypto

To configure `coins`(bitcoin:BTC,ethereum:ETH,cardano:ADA...\*), `vs_currency`(gbp\*) and `days`(1\*) in configuration.cfg
- `coins` can be a list that will be cycled through. Follow convention
- `refresh_interval_seconds` becomes the timer for how long each crypto in the list is shown for 

Find CoinGecko api info here https://www.coingecko.com/en/api/documentation with currency_id at /coins/list and vs_currency at /simple/supported_vs_currencies

\* Current values

# Zero BTC Screen

Bitcoin (or any other currency) stock price for your RPi Zero

![display](docs/display.jpg)

## Hardware

### Platform

* Raspberry Pi Zero W
* Raspberry Pi 3b+
* Raspberry Pi 4
* Any other modern RPi

### Supported displays

* Waveshare eInk types:
  * epd2in13v2
  * epd2in13v3
  * epd2in13bv3
  * epd2in7
  * epd3in7
* inkyWhat (Red, Black, White)
* Virtual (picture)

## Installation

1. Turn on SPI via `sudo raspi-config`
    ```
    Interfacing Options -> SPI
    ```
2. Download Zero BTC Screen
    ```
    git clone https://github.com/StephenR19/zero-btc-screen.git ~/zero-btc-screen
    cd ~/zero-btc-screen
    ```
3. Create and activate venv
    ```
    python3 -m venv venv --system-site-packages
    source venv/bin/activate
    ```
4. Install dependencies
    ```
    pip install rpi-lgpio spidev Pillow numpy
    ```
5. Install drivers for your display
    - Waveshare: `git clone https://github.com/waveshare/e-Paper.git ~/e-Paper && pip install ~/e-Paper/RaspberryPi_JetsonNano/python/`
    - Inky: `pip install inky[rpi]`
6. **Important**: Add CoinGecko API key to `configuration.cfg` under `[base]`:
    ```
    api_key = YOUR_API_KEY_HERE
    ```
7. Test it
    ```
    python main.py
    ```
8. Set up systemd service (see Autostart section)


## Screen configuration

The application supports multiple types of e-ink screens, and an additional "picture" screen.

To configure which display(s) to use, configuration.cfg should be modified. In the following example an e-ink epd2in13v2
and "picture" screens are select:

```cfg
[base]
console_logs             : false
#logs_file               : /tmp/zero-btc-screen.log
dummy_data               : false
refresh_interval_minutes : 15
currency                 : BTC

# Enabled screens or devices
screens : [
    epd2in13v2
#    epd2in13v3
#    epd2in13bv3
#    epd2in7
#    epd3in7
    picture
#    inkyWhatRBW
  ]

# Configuration per screen
# This doesn't make any effect if screens are not enabled above
[epd2in13v2]
mode : candle

[epd2in13v3]
mode : candle

[epd2in13bv3]
mode : line

[epd2in7]
mode : candle

[epd3in7]
mode : candle

[picture]
filename : /home/pi/output.png

[inkyWhatRBW]
mode : candle
```

### Autostart

To make it run on startup you can choose from 2 options:

1. Using the rc.local file
    1. `sudo nano /etc/rc.local`
    2. Add one the following before `exit 0`
   ```
   /usr/bin/python3 /home/pi/zero-btc-screen/main.py &
   ```
   conversely, you can run in `screen` you can install it with `sudo apt-get install screen`
   ```
   su - pi -c "/usr/bin/screen -dm sh -c '/usr/bin/python3 /home/pi/zero-btc-screen/main.py'"
   ```
2. Using the system's services daemon
    1. Create a new service configuration file
       ```
        sudo nano /etc/systemd/system/btc-screen.service
        ```
    2. Copy and paste the following into the service configuration file and change any settings to match your
       environment
       ```
        [Unit]
        Description=zero-btc-screen
        After=network.target
 
        [Service]
        ExecStart=/home/pi/zero-btc-screen/venv/bin/python -u /home/pi/zero-btc-screen/main.py
        WorkingDirectory=/home/pi/zero-btc-screen
        StandardOutput=inherit
        StandardError=inherit
        Restart=always
        User=pi
 
        [Install]
        WantedBy=multi-user.target
        ```
    3. Enable the service so that it starts whenever the RPi is rebooted
       ```
        sudo systemctl enable btc-screen.service
       ```
    4. Start the service and enjoy!
       ```
        sudo systemctl start btc-screen.service
       ```

       If you need to troubleshoot you can use the logging configurations of this program (mentioned below).
       Alternatively, you can check to see if there is any output in the system service logging.
       ```
        sudo journalctl -f -u btc-screen.service
       ```

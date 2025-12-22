# Simple Python script to use a DHT22/11 sensor with a Raspberry Pi

## libraries installation dht22/dht11
```
pip3 install adafruit-circuitpython-dht RPi.GPIO
```

## executable creation
```
pip3 install pyinstaller
pyinstaller dht22main.py --onefile
```
the executable is created in the dist folder
## run as systemd service
create the file:
```sudo nano /etc/systemd/system/dht22main.service```


```
[Unit]
Description=DHT22 sensor reading service
After=default.target

[Service]
Type=simple
User=user
Group=group
WorkingDirectory=/home/user/path/dht22
ExecStart=/home/user/path/dht22/dht22main
Restart=always

[Install]
WantedBy=default.target
```

```
chmod +x /home/user/path/dht22/dht22main
sudo systemctl daemon-reload
sudo systemctl enable dht22main.service
sudo systemctl start dht22main.service
sudo systemctl status dht22main.service
```

Set in the dht.conf file:

delay - the time interval between readings in seconds

print_on_terminal - whether readings should be printed to terminal (useless if running with systemd)

save_to_file - whether to save readings to disk
## run from cli
```python3 dht22main.py```

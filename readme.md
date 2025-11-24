# Simple Python script to use a DHT22/11 sensor with a Raspberry Pi

## library installation dht22/dht11
```
pip3 install adafruit-circuitpython-dht RPi.GPIO
```

## executable creation
```
pip3 install pyinstaller
pyinstaller dht22.py --onefile
```
the executable is created in the dist folder
## run as systemd service
create the file:
```sudo nano /etc/systemd/system/dht22.service```


```
[Unit]
Description=DHT22 sensor reading service
After=default.target

[Service]
Type=simple
User=user
Group=group
WorkingDirectory=/home/user/path/dht22
ExecStart=/home/user/path/dht22/dht22
Restart=always

[Install]
WantedBy=default.target
```

```
chmod +x /home/user/path/dht22/dht22
sudo systemctl daemon-reload
sudo systemctl enable dht22.service
sudo systemctl start dht22.service
sudo systemctl status dht22.service
```

Set in the dht.conf file:

delay - the time interval between readings in seconds

print_on_terminal - whether readings should be printed to terminal (useless if running with systemd)

save_to_file - whether to save readings to disk

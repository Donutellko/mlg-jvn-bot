

# How to run:

```sh
echo "YOUR_TOKEN_FROM_BotFather" > token.txt 

python3 -m venv ./venv
pip install -r requirements.txt

./venv/bin/python mlg_jvn_bot.py
```


# How to reate a daemon

Create file `/etc/systemd/system/my_mlg_jvn_bot.service` with the following content (change `<path_to>`):
```
[Service]
WorkingDirectory=/home/user/<path_to>/tgtg-bot/
ExecStart=/home/user/<path_to>/tgtg-bot/venv/bin/python mlg_jvn_bot.py

User=root

Restart=always

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl start my_mlg_jvn_bot.service
systemctl status my_mlg_jvn_bot.service
sudo journalctl -u my_mlg_jvn_bot.service
```


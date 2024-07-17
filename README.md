Made by Iohann Tachy
Tested on Zabbix version 6.0 LTS.

This template uses a Python script with Selenium to log into the Web Maintenance Console and get the status of an E1 board.

This approach was taken because this information isn't available on SNMP.

(You may need to change the Zabbix trigger parameters depending on the language defined on your Web Maintenance Console.)


Requeriments:
```bash
apt-get install python3 python3-pip -y
```

```bash
pip3 install selenium requests
```

Google Chrome is also required.
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
```
# 📕 Service/Daemon

{% hint style="info" %}
This is the newest type of hosting option
{% endhint %}



## ≡ What is Service/Daemon?

Service also referred as daemon is a process which runs in the background. This process is managed by systemd and can automatically be started on boot. Systemd also tries to restart it if failed. Overall the restart and management of a process is handled by systemd.

## ≡ Why Service/Daemon?

* Its lightweight than docker.&#x20;
* More native to the computer.&#x20;
* Uses less resources

## ≡ Requirements

* PC/Laptop with Linux OS which uses systemd as its system and service manager.\
  Run the following command to check.

```bash
ps -p 1 -o comm=
```

If the output is systemd then you can continue to follow the setup steps

## ≡ How to Host?

### 〣 Clone the repo

```bash
git clone https://github.com/TgCatUB/catuserbot
```

### 〣 _**Setup Chromium & its driver**_

* First check chromium is installed or not

```bash
which chromium
```

If the above command return a path like `/usr/bin/chromium`  (maybe different path if you installed it else where) put that path in .env files.\
If it dosen't return this path follow the following steps to install chromium

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="files"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><em><mark style="color:blue;"><strong>Install Chromium or Google-Chrome</strong></mark></em></td><td></td><td><a href="../../.gitbook/assets/chromium_pokemon.jpg">chromium_pokemon.jpg</a></td><td><a href="../guide/chromium-or-chrome-setup.md#chromium">#chromium</a></td></tr></tbody></table>

### 〣 _**Edit the .env with your config values**_ <a href="#edit-config" id="edit-config"></a>

* Copy .env.smaple to .env file by `cp .env.sample .env`
* Modify the <mark style="color:green;">.env</mark> with any text editor, like `nano .env`
* Do not add data base url in .env file, the script will make a database itslef
* **Check :** [<mark style="color:blue;">**Config Values**</mark>](../variables/config-vars.md#mandatory-vars)

### 〣 Creating service

```bash
sudo python3 install_as_service.py
```

sudo is needed for this command to make the `.service` file and place it in `/etc/systemd/system/` directory.\
Apart from this the script also installs things like uv, progetsql, and requirements.txt .

It is advised to check `install_as_service.py` and `install`_`_`_`checker.py` file before you run them. If you have cloned the repo for correct official source no need to worry.

### 〣 Monitoring and basic operations

* To check status of service

```bash
systemctl status catuserbot.service
```

* To restart the service

```bash
systemctl restart catuserbot.service
```

* To stop the service

```bash
systemctl stop catuserbot.service
```

* To start the service

```bash
systemctl start catuserbot.service
```

* To see journal logs

```bash
sudo journalctl -u catuserbot.service
```

Logs are also stored in the .log file in the root directory of the clone repo

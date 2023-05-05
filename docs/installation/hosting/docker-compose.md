# Docker Compose

## ≡ Run your bot in docker with just simple steps

### 〣 _**Install required packages**_ <a href="#install-packages" id="install-packages"></a>

{% code title="Install git & docker compose" overflow="wrap" %}
```batch
sudo apt install --no-install-recommends -y git docker-compose
```
{% endcode %}

### 〣 _**Clone the repo & make config**_ <a href="#clone-repo" id="clone-repo"></a>

{% code title="Change dir to catuserbot & make config.py to save config values" overflow="wrap" %}
```batch
git clone -b beta https://github.com/TgCatUB/catuserbot && cd catuserbot && mv exampleconfig.py config.py
```
{% endcode %}

### 〣 _**Edit the config.py with your config values**_ <a href="#edit-config" id="edit-config"></a>

* Modify the <mark style="color:green;">config.py</mark> with any text editor, like `nano config.py`
* **Check :** [<mark style="color:blue;">**Config Values**</mark>](../variables/config-vars.md#mandatory-vars)

### 〣 _**All setup completed, its time to run the bot.**_ <a href="#run-bot" id="run-bot"></a>

* _**Run:**_ `sudo docker-compose up`
* _**Run detached:**_ `sudo docker-compose up -d`
* _**Stop:**_ `sudo docker-compose stop`
* _**Check:**_ `sudo docker-compose ps`

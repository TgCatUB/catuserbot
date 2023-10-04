# 📕 Self Host

## ≡ Build your bot manually

{% hint style="warning" %}
Hosting bot manually can be a bit of pain, that why we prefer [<mark style="color:blue;">Docker</mark>](docker-compose.md) over it. Anyways If want to host manually keep up with these 2 pointers: [<mark style="color:blue;">Chrome</mark>](self-host.md#setup-chromium), [<mark style="color:blue;">Venv</mark>](self-host.md#create-venv)
{% endhint %}

### 〣 _**Install required packages**_ <a href="#install-packages" id="install-packages"></a>

{% code title="Update and install apt packages & node.v18" overflow="wrap" %}
```batch
sudo apt update && sudo apt upgrade -y \
&& sudo apt install --no-install-recommends -y ca-certificates curl ffmpeg fonts-noto-color-emoji gcc git gnupg libmagickwand-dev libpq-dev mediainfo nano neofetch pv python3 python3-dev python3-lxml python3-pip python3-psycopg2 screen tree unzip virtualenv wget zlib1g libyaml-dev \
&& curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && NODE_MAJOR=18 && \
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list && \
sudo apt-get update && sudo apt-get install nodejs -y
```
{% endcode %}

### 〣 _**Clone the repo & make config**_ <a href="#clone-repo" id="clone-repo"></a>

{% code title="Change dir to catuserbot & make config.py to save config values" overflow="wrap" %}
```batch
git clone https://github.com/TgCatUB/catuserbot && cd catuserbot && mv exampleconfig.py config.py
```
{% endcode %}

### 〣 _**Setup Chromium & its driver**_ <a href="#setup-chromium" id="setup-chromium"></a>

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-type="select" data-multiple></th><th data-hidden data-card-cover data-type="files"></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><em><mark style="color:blue;"><strong>Install Chromium or Google-Chrome</strong></mark></em></td><td></td><td><a href="../../.gitbook/assets/chromium_pokemon.jpg">chromium_pokemon.jpg</a></td><td><a href="../guide/chromium-or-chrome-setup.md#chromium">#chromium</a></td></tr></tbody></table>

### 〣 _**Edit the config.py with your config values**_ <a href="#edit-config" id="edit-config"></a>

* Modify the <mark style="color:green;">config.py</mark> with any text editor, like `nano config.py`
* **Check :** [<mark style="color:blue;">**Config Values**</mark>](../variables/config-vars.md#mandatory-vars)

### 〣 _**Create a Virtual**_ environment _**& install requirements**_ <a href="#create-venv" id="create-venv"></a>

{% code title="Create catuserbot screen session" overflow="wrap" %}
```batch
screen -S catuserbot
```
{% endcode %}

{% code title="Install venv & requirements" overflow="wrap" %}
```batch
virtualenv venv && source venv/bin/activate && pip3 install -r requirements.txt
```
{% endcode %}

### 〣 _**All setup completed, its time to run the bot.**_ <a href="#run-bot" id="run-bot"></a>

* _**Run:**_ `python3 -m userbot`
* _**Close Screen:**_ Press <mark style="color:red;">CTRL+A</mark> and after that <mark style="color:red;">CTRL+D</mark>
* _**Check:**_ `screen -ls`
* _**Reattach Screen:**_ `screen -r <some_id>.catuserbot`

## ≡ _Video Tutorial_

{% embed url="https://youtu.be/FyfW3-7i5q0" %}
Self Host
{% endembed %}

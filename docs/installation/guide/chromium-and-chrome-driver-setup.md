# 📕 Chromium/Chrome and Chrome driver Setup

{% hint style="info" %}
This setup is only required for the users who followed the SELF-HOST method for deploying Cat Userbot.

This is not required for Docker or Docker-Compose (recommended method) methods.
{% endhint %}

➦ **Why should you do this setup?**

Chromium/Chrome binary and Chrome-driver is a mandatory requirement for many awesome plugins and commands like <mark style="color:green;">AI tools</mark>, <mark style="color:green;">Screenshot</mark>, <mark style="color:green;">Rayso</mark>, <mark style="color:green;">Rayso based logs</mark>, <mark style="color:green;">Carbon</mark>, etc.

Here we will show how to setup this in 2 popular and widely used distros only (<mark style="color:red;">Ubuntu</mark> and <mark style="color:red;">Debian</mark>). Other distro users have to install and setup the Vars accordingly.

{% tabs %}
{% tab title="Ubuntu" %}
{% code title="Install Google Chrome" overflow="wrap" %}
```batch
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add

sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"

sudo apt -y update

sudo apt -y install google-chrome-stable

sudo chmod +x /usr/bin/google-chrome
```
{% endcode %}

{% code title="Installing ChromeDriver" overflow="wrap" %}
```batch
wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip

unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver

sudo chown root:root /usr/bin/chromedriver

sudo chmod +x /usr/bin/chromedriver

rm LICENSE.chromedriver chromedriver_linux64.zip
```
{% endcode %}

{% code title="Download Required Jar Files" overflow="wrap" %}
```batch
wget https://selenium-release.storage.googleapis.com/3.9/selenium-server-standalone-3.9.1.jar

mv selenium-server-standalone-3.9.1.jar selenium-server-standalone.jar
```
{% endcode %}

{% code title="Start Chrome via Selenium Server" overflow="wrap" %}
```batch
screen -S chrome

xvfb-run java -Dwebdriver.chrome.driver=/usr/bin/chromedriver -jar selenium-server-standalone.jar
```
{% endcode %}

After this, do <mark style="color:red;">CTRL+C</mark> then <mark style="color:red;">CTRL+A</mark> and <mark style="color:red;">CTRL+D</mark> to exit screen.

{% code title="Go to catuserbot directory and open the config.py " overflow="wrap" %}
```batch
nano config.py
```
{% endcode %}

{% code title="Add these two vars in your config" overflow="wrap" %}
```batch
CHROME_BIN = "/usr/bin/google-chrome"
CHROME_DRIVER = "/usr/bin/chromedriver"
```
{% endcode %}

Now to save use <mark style="color:red;">Ctrl+O</mark> and press <mark style="color:red;">Enter</mark> , then use <mark style="color:red;">Ctrl+X</mark> to exit.
{% endtab %}

{% tab title="Debian" %}
{% code title="Install chromium and chromium based chrome driver" overflow="wrap" %}
```batch
sudo apt install chromium chromium-driver
```
{% endcode %}

{% code title="Go to catuserbot directory and open the config.py " overflow="wrap" %}
```batch
nano config.py
```
{% endcode %}

{% code title="Add these two vars in your config" overflow="wrap" %}
```batch
CHROME_BIN = "/usr/bin/chromium"
CHROME_DRIVER = "/usr/bin/chromedriver"
```
{% endcode %}

Now to save use <mark style="color:red;">Ctrl+O</mark> and press <mark style="color:red;">Enter</mark> , then use <mark style="color:red;">Ctrl+X</mark> to exit.
{% endtab %}
{% endtabs %}

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

{% content-ref url="../hosting/self-host.md" %}
[self-host.md](../hosting/self-host.md)
{% endcontent-ref %}

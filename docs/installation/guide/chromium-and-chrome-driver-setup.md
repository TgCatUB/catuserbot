# 📕 Chromium and Chrome driver Setup

{% hint style="info" %}
This setup is only required for the users who followed the SELF-HOST method for deploying Cat Userbot.

This is not required for Docker or Docker-Compose (recommended method) methods.
{% endhint %}

➦ **Why should you do this setup?**

Chromium binary and Chrome-driver is a mandatory requirement for many awesome plugins and commands like <mark style="color:green;">AI tools</mark>, <mark style="color:green;">Screenshot</mark>, <mark style="color:green;">Rayso</mark>, <mark style="color:green;">Rayso based logs</mark>, <mark style="color:green;">Carbon</mark>, etc.

Here we will show how to setup this in 2 popular and widely used distros only (<mark style="color:red;">Ubuntu</mark> and <mark style="color:red;">Debian</mark>). Other distro users have to install and setup the Vars accordingly.

{% tabs %}
{% tab title="Ubuntu" %}
{% code title="Install chromium and chromium based chrome driver" overflow="wrap" %}
```batch
sudo apt install chromium-browser chromium-chromedriver
```
{% endcode %}

{% code title="Go to catuserbot directory and open the config.py " overflow="wrap" %}
```batch
nano config.py
```
{% endcode %}

{% code title="Add these two vars in your config" overflow="wrap" %}
```batch
CHROME_BIN = "/usr/bin/chromium-browser"
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

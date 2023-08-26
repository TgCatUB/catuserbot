# 📕 Chromium/Chrome Setup

{% hint style="info" %}
This setup is only required for the users who followed the SELF-HOST method for deploying Cat Userbot.

This is not required for Docker or Docker-Compose (recommended method) methods.
{% endhint %}

➦ **Why should you do this setup?**

**Chromium / Chrome** binary is a mandatory requirement for many awesome plugins and commands like <mark style="color:green;">AI tools</mark>, <mark style="color:green;">Screenshot</mark>, <mark style="color:green;">Rayso</mark>, <mark style="color:green;">Rayso based logs</mark>, <mark style="color:green;">Carbon</mark>, etc.

Here we will show how to setup this for <mark style="color:red;">Debian</mark>, <mark style="color:orange;">Ubuntu</mark>, <mark style="color:blue;">Arch</mark>, <mark style="color:purple;">Fedora</mark> and their derivatives.

{% tabs %}
{% tab title="Chromium" %}
{% code title="For Debian" overflow="wrap" %}
```batch
sudo apt install chromium
```
{% endcode %}

{% code title="For Ubuntu" overflow="wrap" %}
```batch
sudo apt install chromium-browser
```
{% endcode %}

{% code title="For Arch" overflow="wrap" %}
```batch
sudo pacman -S chromium
```
{% endcode %}

{% code title="For Fedora" overflow="wrap" %}
```batch
sudo dnf install chromium
```
{% endcode %}

{% code title="Go to catuserbot directory and open the config.py " overflow="wrap" %}
```batch
nano config.py
```
{% endcode %}

{% code title="Add this one var in your config" overflow="wrap" %}
```batch
CHROME_BIN = "/usr/bin/chromium"
```
{% endcode %}

Now to save use <mark style="color:red;">Ctrl+O</mark> and press <mark style="color:red;">Enter</mark> , then use <mark style="color:red;">Ctrl+X</mark> to exit.
{% endtab %}

{% tab title="Chrome" %}
{% code title="For Debian and Ubuntu" %}
```batch
sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google.list && \
  sudo apt-get update -y && \
  sudo apt-get install -y google-chrome-stable xvfb libxi6 libgconf-2-4 default-jdk && \
  sudo chmod +x /usr/bin/google-chrome
```
{% endcode %}

{% code title="For Arch, you can use any AUR helper, here we" overflow="wrap" %}
```batch
sudo yay -S google-chrome
```
{% endcode %}

{% code title="For Fedora" overflow="wrap" %}
```batch
sudo dnf install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
```
{% endcode %}

{% code title="Go to catuserbot directory and open the config.py" overflow="wrap" %}
```batch
nano config.py
```
{% endcode %}

{% code title="Add this one var in your config" overflow="wrap" %}
```batch
CHROME_BIN = "/usr/bin/google-chrome"
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

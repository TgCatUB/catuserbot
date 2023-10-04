# 📕 Genius API Token

## 〣 Creating an API Client to get Access Token

* Go to [genius.com/api-clients/new](https://genius.com/api-clients/new)
* Click on the "Sign Up" button and Create an Account.
* Enter a name for your App and put `https://example.com` in <mark style="color:green;">APP WEBSITE URL</mark>. You can Leave other two fields empty.

    <figure><img src="https://graph.org/file/d29c51db868599ab7a20f.jpg" alt="Page after clicking 'Create Account' and filling values"><figcaption><p>Page after clicking 'Create Account' and filling values</p></figcaption></figure>

* Click on Save button.

    <figure><img src="https://graph.org/file/051dc8c0530872e0b783d.jpg" alt="Page after clicking 'Save' button"><figcaption><p>Page after clicking 'Save' button</p></figcaption></figure>
    
* On This page, click on <mark style="color:blue;">Generate Access Token</mark> and Copy the token. Save the copied token in your bot's configuration file as environment variable with the following name:
  * `GENIUS_API_TOKEN`

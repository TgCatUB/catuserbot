# 📕 Genius API Token

## 〣 Creating an API Client to get Access Token

* Go to [genius.com/api-clients/new](https://genius.com/api-clients/new)
* Click on the "Sign Up" button and Create an Account.
* Enter a name for your App and put `https://example.com` in <mark style="color:green;">APP WEBSITE URL</mark>. You can Leave other two fields empty.

    <figure><img src="../.gitbook/assets/genius1.jpg" alt="Page after clicking 'Create Account' and filling values"><figcaption><p>Page after clicking 'Create Account' and filling values</p></figcaption></figure>

* Click on Save button.

    <figure><img src="../.gitbook/assets/genius2.jpg" alt="Page after clicking 'Save' button"><figcaption><p>Page after clicking 'Save' button</p></figcaption></figure>
    
* On This page, click on <mark style="color:blue;">Generate Access Token</mark> and Copy the token. Save the copied token in your bot's configuration file as environment variable with the following name:
  * `GENIUS_API_TOKEN`

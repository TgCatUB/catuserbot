# 📕 Spotify

## 〣 Creating a Spotify App

* Go to [developer.spotify.com/dashboard/login](https://developer.spotify.com/dashboard/login) and log in with your Spotify account.
*   Click on the "Create An App" button. This will take you to a page where you can create a new Spotify app.



    <figure><img src="../.gitbook/assets/soptify1.jpg" alt=""><figcaption><p>Page after clicking 'Create an App'</p></figcaption></figure>



*   Enter a name for your app, a short description, and agree to the terms and conditions. Then, click the "Create" button.



    <figure><img src="../.gitbook/assets/soptify2.jpg" alt=""><figcaption><p>Page after clicking 'Create' button</p></figcaption></figure>
* On the next page, you'll see your new app's Client ID and Client Secret. These are the credentials that your bot will use to access the Spotify API. Copy these credentials and save them in your bot's configuration file as environment variables with the following names:
  * `SPOTIFY_CLIENT_ID`
  * `SPOTIFY_CLIENT_SECRET`

## 〣 Setting up Spotify integration with the bot

*   After starting your bot, go to your bot log group in Telegram and type `.spsetup` it will generate a message with a link.



    <figure><img src="../.gitbook/assets/soptify3.jpg" alt=""><figcaption><p>Page after typing .spsetup in Logger group</p></figcaption></figure>
*   Click on the link in the message to open the Spotify authorization page. This is where you will authorize your bot to access your Spotify account.



    <figure><img src="../.gitbook/assets/soptify4.jpg" alt=""><figcaption><p>Page that came after clicking the link of the Logger group</p></figcaption></figure>
* Log in to your Spotify account if you haven't already. Then, click the "Agree" button to give your bot permission to access your Spotify account.  After granting permission, you will be redirected to a blank page, Copy the URL of this page.



*   Go back to your bot log group in Telegram and paste the URL you just copied as a reply to the `.spsetup` message. The bot will use this URL to authenticate with Spotify.



    <figure><img src="../.gitbook/assets/soptify5.jpg" alt=""><figcaption><p>Page after copy pasting the website link in reply of the link of Logger group .</p></figcaption></figure>
* If the authentication is successful, the bot will respond with a message saying "Done! Setup Successful". Your bot is now authorized to access your Spotify account, and you can start using the Spotify commands in your Telegram chats.


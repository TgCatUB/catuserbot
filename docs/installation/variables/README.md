# 📕 Variables

## ≡  What are these ?

Variables are used to store configuration settings and temporary data during the execution of commands. They are defined in <mark style="color:green;">config.py</mark> file and can be customized by users.

In catuserbot there is two types of variables: [<mark style="color:blue;">**Config Variables**</mark>](config-vars.md) & [<mark style="color:blue;">**Database Variables**</mark>](database-vars.md) , understanding how variables work is crucial for customizing the bot to specific needs.

## ≡  Where it save the data?

The database variables are get saved to your database that you set with [<mark style="color:blue;">**DB\_URI**</mark>](config-vars.md#db\_uri) & the config variables are get saved to either <mark style="color:green;">config.py</mark> or in your <mark style="color:green;">app environment</mark> depending [<mark style="color:blue;">**ENV**</mark>](config-vars.md#env) variable.

## ≡  How to save var?

You can edit your <mark style="color:green;">config.py</mark> or in your <mark style="color:green;">app environment</mark> manually or can set by using bot itself ny doing <mark style="color:yellow;">`.set var <Variable-Name> <Value>`</mark> check <mark style="color:yellow;">`.help var`</mark> for more info on this.

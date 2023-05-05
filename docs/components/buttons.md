# Buttons

Buttons are used to perform actions in the product.

## Default

{% embed url="https://5ccbc373887ca40020446347-geedzbiswp.chromatic.com/iframe.html?id=button--basic&args=size:medium;containsIcon:false&viewMode=story" %}

{% hint style="info" %}
**Good to know:** you can embed a Storybook canvas by simple pasting the canvas link and hitting enter.
{% endhint %}

```
<Button
    label="Label"
    size="medium"
    kind="default"
    onClick={doTheThing}
/>
```

## Primary

{% embed url="https://5ccbc373887ca40020446347-geedzbiswp.chromatic.com/iframe.html?id=button--basic&args=size:medium;containsIcon:false;appearance:primary&viewMode=story" %}

```javascript
<Button
    label="Label"
    size="medium"
    kind="primary"
    onClick={doTheThing}
/>
```

## Secondary

{% embed url="https://5ccbc373887ca40020446347-geedzbiswp.chromatic.com/iframe.html?id=button--basic&args=size:medium;containsIcon:false;appearance:secondary&viewMode=story" %}

```javascript
<Button
    label="Label"
    size="medium"
    kind="secondary"
    onClick={doTheThing}
/>
```

_These examples are taken from the excellent_ [Storybook Example Design System](https://5ccbc373887ca40020446347-geedzbiswp.chromatic.com/?path=/story/icon--labels)_._

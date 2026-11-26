import asyncio
import httpx

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "tools"

TICKER_ALIASES = {
    # Forex
    "EURUSD": ("EUR/USD", "EURUSD=X"),
    "GBPUSD": ("GBP/USD", "GBPUSD=X"),
    "USDINR": ("USD/INR", "USDINR=X"),
    "USDJPY": ("USD/JPY", "USDJPY=X"),
    "AUDUSD": ("AUD/USD", "AUDUSD=X"),
    "USDCAD": ("USD/CAD", "USDCAD=X"),
    "USDCHF": ("USD/CHF", "USDCHF=X"),
    # Commodities / Metals
    "GOLD": ("Gold (1 oz)", "GC=F"),
    "XAU": ("Gold (1 oz)", "GC=F"),
    "SILVER": ("Silver (1 oz)", "SI=F"),
    "XAG": ("Silver (1 oz)", "SI=F"),
    "OIL": ("Crude Oil (WTI)", "CL=F"),
    "CRUDE": ("Crude Oil (WTI)", "CL=F"),
    # Crypto
    "BTC": ("Bitcoin", "BTC-USD"),
    "BTCUSD": ("Bitcoin (USD)", "BTC-USD"),
    "ETH": ("Ethereum", "ETH-USD"),
    "ETHUSD": ("Ethereum (USD)", "ETH-USD"),
    "SOL": ("Solana", "SOL-USD"),
    "SOLUSD": ("Solana (USD)", "SOL-USD"),
    "DOGE": ("Dogecoin", "DOGE-USD"),
}

DEFAULT_PAIRS = [
    ("EUR/USD", "EURUSD=X"),
    ("GBP/USD", "GBPUSD=X"),
    ("USD/INR", "USDINR=X"),
    ("USD/JPY", "USDJPY=X"),
    ("Gold (1 oz)", "GC=F"),
    ("Silver (1 oz)", "SI=F"),
    ("Crude Oil", "CL=F"),
    ("Bitcoin", "BTC-USD"),
    ("Ethereum", "ETH-USD"),
    ("Solana", "SOL-USD"),
]


async def fetch_yahoo_quote(client, display_name, ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("chart", {}).get("result")
            if result and len(result) > 0:
                meta = result[0].get("meta", {})
                price = meta.get("regularMarketPrice")
                prev_close = meta.get("chartPreviousClose", price)
                currency = meta.get("currency", "USD")
                day_high = meta.get("regularMarketDayHigh")
                day_low = meta.get("regularMarketDayLow")

                if price is not None:
                    change_pct = ((price - prev_close) / prev_close) * 100 if prev_close else 0
                    return {
                        "name": display_name,
                        "ticker": ticker,
                        "price": price,
                        "prev_close": prev_close,
                        "currency": currency,
                        "change_pct": change_pct,
                        "day_high": day_high,
                        "day_low": day_low,
                    }
    except Exception as e:
        LOGS.debug(f"Failed to fetch {ticker}: {e}")
    return None


@catub.cat_cmd(
    pattern=r"forex(?:\s|$)([\s\S]*)",
    command=("forex", plugin_category),
    info={
        "header": "Get live Forex, Commodity (Gold/Silver), and Crypto market quotes.",
        "description": "Fetches real-time price rates and daily changes without requiring any API key.",
        "usage": [
            "{tr}forex",
            "{tr}forex <pair/symbol>",
        ],
        "examples": [
            "{tr}forex",
            "{tr}forex gold",
            "{tr}forex gbpusd",
            "{tr}forex btc",
            "{tr}forex silver",
        ],
    },
)
async def forex_cmd(event):
    "Live Forex & Market quotes."
    input_str = event.pattern_match.group(1).strip().upper()
    catevent = await edit_or_reply(event, "`Fetching live market quotes...`")

    async with httpx.AsyncClient(timeout=10) as client:
        # Case 1: Overview Dashboard (no specific pair provided)
        if not input_str:
            tasks = [fetch_yahoo_quote(client, name, ticker) for name, ticker in DEFAULT_PAIRS]
            quotes = await asyncio.gather(*tasks)

            lines = ["📊 **Global Forex & Markets Overview**\n"]
            for q in quotes:
                if q:
                    sign = "+" if q["change_pct"] >= 0 else ""
                    emoji = "🟢" if q["change_pct"] >= 0 else "🔴"
                    price_str = f"{q['price']:,.2f}" if q["price"] >= 1 else f"{q['price']:.4f}"
                    lines.append(f"• **{q['name']}**: `{price_str} {q['currency']}` ({emoji} `{sign}{q['change_pct']:.2f}%`)")

            lines.append("\n💡 _Tip: Use `.forex <symbol>` (e.g. `.forex gold`, `.forex btc`, `.forex gbpusd`) for details._")
            return await catevent.edit("\n".join(lines))

        # Case 2: Specific Pair Query
        clean_key = input_str.replace("/", "").replace("-", "").replace(" ", "")
        if clean_key in TICKER_ALIASES:
            display_name, ticker = TICKER_ALIASES[clean_key]
        else:
            # Heuristic: standard 6-char currency pair (e.g., EURGBP) -> EURGBP=X
            if len(clean_key) == 6 and clean_key.isalpha():
                display_name = f"{clean_key[:3]}/{clean_key[3:]}"
                ticker = f"{clean_key}=X"
            else:
                display_name = input_str
                ticker = clean_key

        quote = await fetch_yahoo_quote(client, display_name, ticker)
        if not quote:
            return await edit_delete(
                catevent,
                f"__Could not find market data for `{input_str}`. Try e.g. `.forex gold`, `.forex gbpusd`, or `.forex btc`.__",
                time=10,
            )

        sign = "+" if quote["change_pct"] >= 0 else ""
        emoji = "🟢" if quote["change_pct"] >= 0 else "🔴"
        price_str = f"{quote['price']:,.2f}" if quote["price"] >= 1 else f"{quote['price']:.4f}"

        details = [
            f"📈 **Market Quote:** **{quote['name']}** (`{quote['ticker']}`)",
            f"• **Price:** `{price_str} {quote['currency']}`",
            f"• **24h Change:** {emoji} `{sign}{quote['change_pct']:.2f}%`",
        ]
        if quote.get("day_high") is not None and quote.get("day_low") is not None:
            high_str = f"{quote['day_high']:,.2f}" if quote["day_high"] >= 1 else f"{quote['day_high']:.4f}"
            low_str = f"{quote['day_low']:,.2f}" if quote["day_low"] >= 1 else f"{quote['day_low']:.4f}"
            details.append(f"• **24h Range:** `{low_str}` - `{high_str}`")

        await catevent.edit("\n".join(details))

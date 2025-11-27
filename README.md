# Crypto Price Alert Bot

A fast and lightweight Telegram bot that notifies you instantly when a cryptocurrency price crosses your target (using Binance USDT pairs).

## Features
- `/up BTC 65000` → alerts when price goes above 65,000  
- `/down ETH 3000` → alerts when price drops below 3,000  
- `/list` → show all your active alerts  
- `/clear` → remove all alerts  
- `/price SOL` → get current price  
- Runs every 15 seconds, no heavy database  

## Status
**In active development**  
I'm currently learning and improving the bot every day — expect frequent commits!

## Tech Stack
- Python 3.12+
- aiogram 3.x
- aiohttp
- Binance Public API

## Roadmap
- [x] Basic up/down alerts
- [x] Smart mistake detection
- [ ] Persistent alerts (JSON → SQLite)
- [ ] Bulk price fetching (one request instead of many)
- [ ] WebSocket support (real-time, no polling)
- [ ] Deploy on VPS / Docker

Contributions, suggestions and stars are very welcome!

Made with love while learning

---

*Last updated: Nov 2025*

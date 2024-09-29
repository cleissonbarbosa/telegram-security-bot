# Security Exploits and Notifications Bot

This is a Telegram bot that allows users to search for vulnerabilities using the CVE (Common Vulnerabilities and Exposures) and receive notifications about recent security vulnerabilities.

Available languages: [see the list of supported languages](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages)

## Features

- **/exploit `<CVE-ID>` `<LANGUAGE>`**: Searches for details of a specific vulnerability by ID, including description and references.
    - `<CVE-ID>` is required
    - `<LANGUAGE>` is optional (default is English)
- **/recent `<LANGUAGE>`**: Returns a list of the most recent vulnerabilities available.
    - `<LANGUAGE>` is optional (default is English)
- **/start**: Displays a welcome message and usage instructions.

---

## How to Create a Bot and Obtain a Token 🛠️

To use this bot, you need to create your own bot on Telegram and obtain the access token. Follow the steps below:

1. **Access Telegram** and search for the bot called [BotFather](https://t.me/BotFather).
2. **Start a conversation with BotFather** by sending `/start`.
3. **Create a new bot** by sending the command `/newbot` and follow the provided instructions. You will need to choose a name and a username for your bot.
4. After creating the bot, BotFather will provide an **API Token**. The token will look something like this: `123456789:ABCdefGhIJKlmnOPqRsTuVWXyz`.

### How to Use the Token in the Code

Replace `YOUR_TELEGRAM_BOT_TOKEN` in the code with the token you obtained from BotFather:

```python
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
```

---

## How to Run the Bot 🚀

#### 1. Clone the Repository

```bash
git clone https://github.com/cleissonbarbosa/telegram-security-bot
cd telegram-security-bot
```

#### 2. Install Dependencies:

Make sure you have Python installed and then run:

```bash
pip install -r requirements.txt
```

#### 3. Run the Bot:

After configuring the token and installing the dependencies, you can run the bot with the following command:

```bash
python src/main.py
```

---

## Future Improvements 🔮

- [ ] Add support for searching vulnerabilities by keywords.
- [ ] Automatic notifications of vulnerabilities at defined intervals.
- [ ] Integration with other security APIs.
- [ ] Advanced filters for CVE searches.

---

## Contributions 🤝

Contributions are welcome! Feel free to open issues and pull requests with suggestions or improvements.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

# GorkBot

A feature-rich Discord bot built on python with `discord.py`, featuring a dynamic localization system, music playback, and League of Legends utility commands.

Yes, its name comes from the AI agent.

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for audio processing and downloads. Ensure it is added to your system's `PATH`.
- **MySQL/MariaDB**: A database instance to store server settings and user profiles.

### Installation

1. Clone the repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory to store your sensitive credentials:

```env
TOKEN=your_discord_bot_token_here

# Database Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASS=your_database_password
DB_NAME=your_database_name
```

### Database Setup
The bot uses an asynchronous MySQL pool (`aiomysql`). Upon startup, the bot will automatically execute the `create_tables()` method from `database.py` to initialize:
- `botsettings`: Stores per-guild prefixes and language preferences.
- `leagueconfig`: Maps Discord IDs to Riot IDs.

## 🌍 Localization (JSON Structure)

The bot supports multiple languages located in the `bot/languages/` directory. The structure follows a `{language}/{category}/{command}.json` pattern.

### How it works:
The `languageservice` helper dynamically loads the appropriate JSON based on the server's configured language (defaulting to English).

### JSON Example (`lolgen.json`):
```json
{
    "champions": ["List", "of", "names"],
    "roles": ["Top", "Jungle", "..."],
    "messages": {
        "challenge_title": "Translated String",
        "error_loading_data": "Error message here"
    }
}
```
To add a new language, create a new folder (e.g., `es` for Spanish) and replicate the folder/file structure of the `en` or `ptbr` directories.

## 🛠️ Usage

To start the bot, run the main entry point:
```bash
python main.py
```
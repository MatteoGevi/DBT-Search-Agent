import asyncio
from bot.bot_handler import BotHandler
from config.config_handler import ConfigHandler

async def main():
    # Initialize configuration
    config = ConfigHandler()
    
    # Print available platforms
    print("Initializing bot with the following platforms:")
    for platform in config.available_platforms:
        print(f"- {platform}")
    
    # Initialize bot handler
    bot = BotHandler()
    
    # Start the bot for each configured platform
    tasks = []
    
    try:
        # Keep the bot running
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down bot...")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 
import application
import dotenv
import os


dotenv.load_dotenv()
_SECRET_TOKEN_NAME = "SECRET_TOKEN"


if __name__ == "__main__":
    print("Starting discord bot.")
    bot = application.init_bot()
    bot.run(os.getenv(_SECRET_TOKEN_NAME))

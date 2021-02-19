from os import getenv

from discord import Intents, User, Message
from dotenv import load_dotenv
from utilsx.discord import BotX
from glob import glob

from src.utils.Logger import Logger

load_dotenv()


class Bot(BotX):
    def __init__(self):
        super().__init__(Intents.all())
        self.prefix = self.get_bot_prefix
        self.description = "Guardian protects your server against NSFW!"

        modules = list(map(lambda extension: extension.replace("/", ".")[:-3], glob("src/modules/*.py")))

        for index, _ in enumerate(self.load_extensions(modules)):
            Logger.info(f"Loaded: {modules[index].replace('src/modules.', '')}")

    async def on_ready(self):
        Logger.info(f"Successfully connected to discord as {self.user}")

    @staticmethod
    def get_bot_prefix(user: User, message: Message):
        return "guardian "


if __name__ == "__main__":
    Bot().run(getenv("BOT_TOKEN"))

from time import time

from discord import Message, File
from nudenet import NudeClassifier, NudeDetector
from utilsx.discord import Cog

from run import Bot
from src.utils.Logger import Logger

image_extensions = [".png", ".jpg", ".jpeg"]
classifier = NudeClassifier()
detector = NudeDetector()


class NSFWProcessor(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        Logger.debug(f"Started processing {message.id}")
        new_images = []
        if message.attachments:
            process = []

            for attachment in message.attachments:
                for extension in image_extensions:
                    if attachment.filename.endswith(extension):
                        process.append(attachment)

            for attachment in process:
                await attachment.save(f"./tmp/{attachment.filename}")
                classification = classifier.classify(f"./tmp/{attachment.filename}")[f"./tmp/{attachment.filename}"]

                if classification["safe"] < classification["unsafe"]:
                    name = f"./tmp/{round(time() * 1000)}-{attachment.filename}"
                    detector.censor(f"./tmp/{attachment.filename}", name)
                    new_images.append(File(name, attachment.filename))

        for image in new_images:
            em = await self.embed(message.channel, f"Auto detected NSFW in message from {message.author.mention}!",
                                  get_embed=True, image=f"attachment://{image.filename}")
            await self.send(message.channel, "", embed=em, file=image)
            await message.delete()

        Logger.debug(f"Successfully processed {message.id}")


def setup(bot: Bot):
    bot.add_cog(NSFWProcessor(bot))

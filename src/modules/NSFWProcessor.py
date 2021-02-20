from time import time

from discord import Message, File
from nudenet import NudeClassifier, NudeDetector
from utilsx.discord import Cog
from utilsx.discord.objects import Footer

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
        if message.author.bot or message.channel.is_nsfw():
            return

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

        if new_images:
            hooks = await message.channel.webhooks()
            sender = None
            for hook in hooks:
                if hook.user == self.bot.user:
                    sender = hook
                    break

            if sender is None:
                sender = await message.channel.create_webhook(name="Guardian",
                                                              reason="No existing webhook was found, creating one!")

            for image in new_images:
                em = await self.embed(sender, "", get_embed=True, image=f"attachment://{image.filename}",
                                      footer=Footer("Auto detected NSFW, removed by Guardian",
                                                    self.bot.user.avatar_url))
                # await self.send(sender, "", embed=em, file=image)
                await sender.send(content=message.content, username=str(message.author),
                                  avatar_url=message.author.avatar_url, file=image, embed=em)
                await message.delete()

        Logger.debug(f"Successfully processed {message.id}")


def setup(bot: Bot):
    bot.add_cog(NSFWProcessor(bot))

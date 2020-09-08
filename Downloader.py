import logging
import wget
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Please Send Link/Image/Video')

def help_command(update, context):
    update.message.reply_text('Help!')

def link(update, context):
    update.message.reply_text("Downloading..")
    try:
        link = update.message.text
        wget.download(link)
        update.message.reply_text("Downloaded Successfully!")
    except ValueError as e:
        update.message.reply_text("Incorrect Link")

def photo(update, context):
    filename = update.message.message_id
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download(str("image_")+str(filename)+".jpg")
    update.message.reply_text("Downloaded to the server")

def video_hand(update, context):
    filename = update.message.message_id
    file_id = update.message.video.file_id
    newFile = context.bot.get_file(file_id)
    newFile.download(str("video_")+str(filename)+"."+update.message.video.mime_type[6:9])
    update.message.reply_text("Downloaded to the server")

def main():
    updater = Updater( os.environ.get('TOKEN', ""), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, link))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(MessageHandler(Filters.video, video_hand))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import os
import qrcode


cwd = os.getcwd()

try :
    os.mkdir(cwd+"/QR_img")
except:
    pass

TOKEN = "******************************************"

async def QR_code_image(url:str):
    out_qr_path = cwd+"/QR_img"+"/qr_img.png"
    qr = qrcode.QRCode(version=1,
                error_correction= qrcode.constants.ERROR_CORRECT_L,
                box_size=50,
                border = 2)

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color = "black", back_color = "white")


    img.save(out_qr_path)

    return out_qr_path

# commands function
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "send your url for convert it to QRcode")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "for any problem you can connect with admin: @A_I_ZONE")

# custom messagw
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    if filters.TEXT.check_update(update):
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "wait for processing...")
        qr = await QR_code_image(text)
        await context.bot.send_document(chat_id = update.effective_chat.id, document = qr)
        os.remove(qr)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

   #commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.run_polling(poll_interval = 3)

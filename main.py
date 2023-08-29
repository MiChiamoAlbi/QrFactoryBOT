from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, filters

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, CircleModuleDrawer
from io import BytesIO
from ast import literal_eval

IMP, CHOSE, FB, ICON, BACK, DIM, COR = range(7)

async def start(update: Update, context: CallbackContext):
    CallbackContext.user_data = [None,None,None,None,None,None] # 0-fill, 1-background, 2-url_image, 3-style, 4-correction, 5-dimension
    await update.message.reply_text("Hey welcome - you can send a message and I will reply with the qrcode\n\nWARNING: some style could potentially not be detected from all qrreader, so before publishing make sure that is working correctly")

async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(text="This bot is created to make your qr codes colored and stylish as they should be. In the future will come more feture!\n\nIf you want make a laugh how bad I code or you want to propose some changes, you can reach me on <a href='https://github.com/MiChiamoAlbi/QrFactoryBOT'>GitHub</a>", parse_mode='HTML')

async def create_qr(update: Update, context: CallbackContext):
    img_io = BytesIO()
    try:
        if CallbackContext.user_data[4] == 'L':
            qr = qrcode.QRCode(
                version=CallbackContext.user_data[5],
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
        elif CallbackContext.user_data[4] == 'H':
            qr = qrcode.QRCode(
                version=CallbackContext.user_data[5],
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
        else:
            qr = qrcode.QRCode(
                version=CallbackContext.user_data[5],
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
    except:
            print('Qualcosa è andato storto')
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )

    qr.add_data(update.message.text)
    qr.make(fit=True)

    try:
        fill_color = (0,0,0)
        if CallbackContext.user_data[0]:
            fill_color = literal_eval(CallbackContext.user_data[0])
        bg_color = (255,255,255)
        if CallbackContext.user_data[1]:
            bg_color = literal_eval(CallbackContext.user_data[1])
    except:
        fill_color = (0,0,0)
        bg_color = (255,255,255)
    try:   
        if CallbackContext.user_data[3] == 'circle':
            img = qr.make_image(color_mask=SolidFillColorMask(front_color=fill_color, back_color=bg_color), image_factory=StyledPilImage, module_drawer = CircleModuleDrawer())
        elif CallbackContext.user_data[3] == 'rounded':
            img = qr.make_image(color_mask=SolidFillColorMask(front_color=fill_color, back_color=bg_color), image_factory=StyledPilImage, module_drawer = RoundedModuleDrawer())
        else:
            img = qr.make_image(fill_color=fill_color, back_color=bg_color)
    except:
        img = qr.make_image(fill_color=fill_color, back_color=bg_color)

    img.save(img_io)
    img_io.seek(0)
    await update.message.reply_photo(img_io)
    

async def settings(update: Update, context: CallbackContext):
    keyboard = [
                    [
                        InlineKeyboardButton("Colours", callback_data="colour"),
                        InlineKeyboardButton("Icon", callback_data="icon"),
                    ],
                    [
                        InlineKeyboardButton("Style", callback_data="style"),
                        InlineKeyboardButton("Dimension", callback_data="dimension"),
                    ],
                    [
                        InlineKeyboardButton("End", callback_data="end"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Settings to edit the style of your qrcodes', reply_markup=reply_markup)
    return IMP

async def back_settings(update: Update, context: CallbackContext):
    keyboard = [
                    [
                        InlineKeyboardButton("Colors", callback_data="colour"),
                        InlineKeyboardButton("Icon", callback_data="icon"),
                    ],
                    [
                        InlineKeyboardButton("Style", callback_data="style"),
                        InlineKeyboardButton("Dimension", callback_data="dimension"),
                    ],
                    [
                        InlineKeyboardButton("End", callback_data="end"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text('Settings to edit the style of your qrcodes', reply_markup=reply_markup)
    except:
        print('no')
        await update.message.reply_text('Settings to edit the style of your qrcodes', reply_markup=reply_markup)
    return IMP

async def front_back(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [
                    [
                        InlineKeyboardButton("Fill", callback_data="fill"),
                        InlineKeyboardButton("Background", callback_data="background"),
                    ],
                    [
                        InlineKeyboardButton("Menu", callback_data="menu"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Settings to edit the style of your qrcodes', reply_markup=reply_markup)
    return FB

async def colour(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [
                    [
                        InlineKeyboardButton("Black", callback_data= query.data + "_(0,0,0)"),
                        InlineKeyboardButton("White", callback_data= query.data + "_(255,255,255)"),
                    ],
                    [
                        InlineKeyboardButton("Yellow", callback_data= query.data + "_(250,250,51)"),
                        InlineKeyboardButton("Red", callback_data= query.data + "_(255,0,0)"),
                    ],
                    [
                        InlineKeyboardButton("Blu", callback_data= query.data + "_(0,0,255)"),
                        InlineKeyboardButton("Green", callback_data= query.data + "_(0,255,0)"),
                    ],
                    [
                        InlineKeyboardButton("Menu", callback_data="menu"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Select the color you prefer', reply_markup=reply_markup)
    return CHOSE

async def save(update: Update, context: CallbackContext):
    query = update.callback_query
    try:
        if not CallbackContext.user_data in globals():
            CallbackContext.user_data = [None,None,None,None,None,None]
    except:
        pass
    if query.data[:4]=='fill':
        CallbackContext.user_data[0]=query.data[5:]
    elif query.data[:10]=='background':
        CallbackContext.user_data[1]=query.data[11:]
    else:
        CallbackContext.user_data[3]=query.data

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Exit", callback_data="end")]
        ])
    await query.answer()
    await query.edit_message_text("Saved", reply_markup=reply_markup)
    return BACK             

async def icon(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Exit", callback_data="end")]
        ])
    await query.answer()
    await query.edit_message_text("This feature will be implemented as soon as posible", reply_markup=reply_markup)
    return BACK

async def style(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [
                    [
                        InlineKeyboardButton("Squared", callback_data="square"),
                    ],
                    [
                        InlineKeyboardButton("Circled", callback_data="circle"),
                    ],
                    [
                        InlineKeyboardButton("Rounded", callback_data="rounded"),
                    ],
                    [
                        InlineKeyboardButton("Menu", callback_data="menu"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Select the style you prefer', reply_markup=reply_markup)
    return CHOSE

async def correction(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
                    [
                        InlineKeyboardButton("L", callback_data="L"),
                        InlineKeyboardButton("M", callback_data="M"),
                        InlineKeyboardButton("H", callback_data="H"),
                    ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text("Select the error correction you want:\n-L About 7% or less errors can be corrected.\n-M About 15% or less errors can be corrected.\n-H About 30% or less errors can be corrected.", reply_markup=reply_markup)
    return COR

async def dimension(update: Update, context: CallbackContext):
    try:
        if not CallbackContext.user_data in globals():
            CallbackContext.user_data = [None,None,None,None,None,None]
    except:
        pass
    query = update.callback_query
    CallbackContext.user_data[4] = query.data
    await query.answer()
    await query.edit_message_text('Insert a dimension between 1, the smallest, to 40, the biggest. You can put None as default')
    return DIM

async def dim_save(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Menu", callback_data="menu")],
        [InlineKeyboardButton("Exit", callback_data="end")]
        ])
    try:
        if update.message.text==None or str(update.message.text).lower()=='none':
            CallbackContext.user_data[5]=None
            await update.message.reply_text('Okay!', reply_markup=reply_markup)
        elif int(update.message.text)<41 or int(update.message.text)>0:
            CallbackContext.user_data[5]=int(update.message.text)
            await update.message.reply_text('Okay!', reply_markup=reply_markup)
        else:
            await update.message.reply_text('Something went wrong', reply_markup=reply_markup)
    except:
        await update.message.reply_text('Something went wrong', reply_markup=reply_markup)
    return BACK

async def end(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("End")
    return ConversationHandler.END

def main(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))

    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("settings", settings)],
            states={
                IMP: [
                    CallbackQueryHandler(front_back, pattern="^colour$"),
                    CallbackQueryHandler(icon, pattern="^icon$"),
                    CallbackQueryHandler(style, pattern="^style$"),
                    CallbackQueryHandler(correction, pattern="^dimension$"),
                    CallbackQueryHandler(end, pattern="^end$"),
                ],
                FB: [
                    CallbackQueryHandler(colour, pattern="fill|background"),
                ],
                CHOSE:[
                    CallbackQueryHandler(save, pattern="^(?!menu$)"),
                ],
                ICON: [
                    #MessageHandler(filters.TEXT, save_link),
                ],
                BACK:[
                    CallbackQueryHandler(back_settings, pattern="^menu$"),
                    CallbackQueryHandler(end, pattern="^end$"),
                ],
                COR:[
                    CallbackQueryHandler(dimension, pattern="^L|M|H$"),
                ],
                DIM:[
                    MessageHandler(filters.TEXT & (~ filters.COMMAND), dim_save),
                ],
            },
            fallbacks=[CallbackQueryHandler(back_settings, pattern="^menu$")],
        )
    )

    application.add_handler(MessageHandler(filters.TEXT & (~ filters.COMMAND), create_qr))
    #application.add_handler(MessageHandler(filters.PHOTO & (~ filters.COMMAND), decode))

if __name__ == "__main__":
    from credentials import TOKEN

    from telegram.ext import Application

    application = Application.builder().token(TOKEN).build()
    main(application)
    application.run_polling()
from aiogram import Router, types,F
from aiogram.filters import CommandStart
from  aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import db, bot
from data.config import ADMINS
from utils.extra_datas import make_title

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan \ qo'yish esdan chiqmasin. Masalan  \.  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """

    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    user = None
    try:
        user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    except Exception as error:
        logger.info(error)
    if user:
        count = await db.count_users()
        msg = (f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    await message.answer(f"Assalomu alaykum {make_title(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.photo)
async def handle_photo(message: types.Message):
    """Foto handler"""
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    await message.answer(
        f"📸 <b>Foto qabul qilindi</b>\n\n"
        f"🗄️ File ID: <code> {photo.file_id}</code>\n"
        f"🦯 O`lcham: {photo.width}x{photo.height}\n"
        f" ⛓️ Hajmi: {photo.file_size//1024} KB\n"
        f" Path : <code>{file_info.file_path}</code>\n\n"
        f" Caption: {message.caption or 'yoq'}\n"
    )
    await message.answer_photo(
        photo.file_id,
        caption="BU sizning rasmingiz"

    )

@router.message(F.video)
async def handle_video(message: types.Message):
    """Video handler"""
    video = message.video
    await message.answer(
        f"📸 <b> video qabul qilindi</b>\n\n"
        f"🗄️ File ID: <code> {video.file_id}</code>\n"
        f"🦯 O`lcham: {video.width}x{video.height}\n"
        f" davomiyligi: {video.duration} Soniya\n"
        f" hajmi: {video.file_size//1024 // 1024} MB\n\n"
        f" Caption: {message.caption or 'yoq'}"

    )


@router.message(F.audio)
async def handle_audio(message: types.Message):
    """Video handler"""
    audio = message.audio
    await message.answer(
        f"📸 <b> audio qabul qilindi</b>\nijrochi: {audio.performer or 'Nomalum'}\n nomi: {audio.title or 'Nomalum'}\n davomiyligi: {audio.duration} Soniya\n hajmi: {audio.file_size // 1024 // 1024} MB"
    )

@router.message(F.voice)
async def handle_voice(message: types.Message):
    """Video handler"""
    voice = message.voice
    await message.answer(
        f"📸 <b> ovozli habar  qabul qilindi</b>\n\n"
        f" ⌚davomiyligi: {voice.duration} Soniya\n"
        f" 📁hajmi: {voice.file_size // 1024 // 1024} MB\n\n"
        f" ovozingz juda yoqimli,😊"
    )


@router.message(F.video_note)
async def handle_video_note(message: types.Message):
    video = message.video_note
    await message.answer(
        f"video habar qabul qilindi \n\n"
        f"Davomiyligi: {message.video_note.duration} Soniya\n "
        f"olchami: {message.video_note.length}x{message.video_note.length}/n"
        f"hajmi : {message.video_note.file_size // 1024} KB \n\n"
        f" Ajoyib video habar!"
    )



@router.message(F.document)
async def handle_document(message: types.Message):
    document = message.document
    await message.answer(
        f" <b> document qabul qilindi</b>\n\n"
        f"Nomi: {document.file_name}\n "
        f"Turi {document.mime_type}\n "
        f"hajmi {document.file_size // 1024 // 1024} KB\n\n"
        f"File ID: <code> {document.file_id}</code>\n\n"
        f"Hujjat muvafaqiyatli yuklandi"

    )
@router.message(F.sticker)
async def handle_sticker(message: types.Message):
    sticker = message.sticker
    await message.answer(
        f"<b>Sticker qabul qlindi!</b>\n\n"
        f"emoji: {sticker.emoji or 'yoq'}\n"
        f"set nomi: {sticker.set_name or 'yoq'}\n"
        f"file ID <code> {sticker.file_id}</code>\n"
        f"Juda zo`r sticker!"
    )
    await message.answer_sticker(sticker.file_id)

@router.message(F.animation)
async def handle_animation(message: types.Message):
    animation = message.animation
    await message.answer(
        f"<b>Animation qabul qilindi!</b>\n\n"
        f"O`lcham:{animation.width}x{animation.height}\n"
        f"davomiyligi: {animation.duration} Soniya\n"
        f"hajmi: {animation.file_size//1024 // 1024} MB\n\n"
        f"Qiziqarli animatsiya!"

    )

@router.message(F.location)
async def handle_location(message: types.Message):
    location = message.location
    await message.answer(
        f"<b>Location qabul qilindi!</b>\n\n"
        f"latitude: {location.latitude}\n\n"
        f"longitude: {location.longitude}\n\n"
        f" Google Maps: https://maps.google.com/maps?q={location.latitude},{location.longitude}\n\n"
        f"rahmat"

    )
@router.message(F.contact)
async def handle_contact(message: types.Message):
    contact = message.contact
    await message.answer(
        f"<b>Contact qabul qilindi!</b>\n\n"
        f"ISm: {contact.first_name}\n"
        f"  familiya :{contact.last_name or 'yoq'}\n"
        f" telefon: {contact.phone_number}\n\n"
        f" User Id : {contact.user_id or 'yoq'}\n\n"
        f"Kontakt saqlandi"
    )
@router.message(F.txt)
async def handle_txt(message: types.Message):
    txt = message.text
    await message.answer(
        f"<b>Matn xabar!</b>\n\n"
        f"{txt}\n\n"
        f"uzunligi: {len(txt)} belgi\n"
        f"Sozlar: {len(txt.split)()} ta\n"
        f"katta harflar: {sum(1 for c in txt if c.issupper())}\n"
        f" kichik harflar:{sum (1 for c in txt if c.islower())}"
    )
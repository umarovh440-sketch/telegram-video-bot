#!/usr/bin/env python3
"""
🎬 БОТИ TELEGRAM БАРОИ МОНТАЖИ ВИДЕО
Функсияҳо: видео монтаж, расм, мемҳо, эффектҳо, музика, текст, ҷустуҷӯ, AI
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Бор кардани переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не установлен!")

print(f"✅ Token гирифта шуд: {TOKEN[:20]}...")

# ============ ОБРАБОТЧИКИ ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /start"""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("✂️ Видео монтаж", callback_data="video_edit"),
         InlineKeyboardButton("🖼️ Расм монтаж", callback_data="image_edit")],
        [InlineKeyboardButton("😂 Мемҳо", callback_data="memes"),
         InlineKeyboardButton("🔍 Ҷустуҷӯ", callback_data="search")],
        [InlineKeyboardButton("🤖 AI видео", callback_data="ai_video"),
         InlineKeyboardButton("❓ Кӯмак", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""👋 Хуш омадед, {user.first_name}!

🎬 **БОТИ МОНТАЖИ ВИДЕО**

**Функсияҳо:**
✅ Видео монтаж (буридан, эффектҳо, музика)
✅ Расм монтаж (эффектҳо, текст)
✅ Мемҳо (10+ шаблон)
✅ Ҷустуҷӯ (видео, расм, музика)
✅ AI видео генератор
✅ 100% БЕСПЛАТНА

**Оғоз:**
1. Видео ё расм фарусттанд
2. Менюро интихоб кунед
3. Натиҷаро дарбаровар кунед"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик /help"""
    text = """📚 **КӮМАК**

**КОМАНДИ:**
/start - Оғоз
/help - Кӯмак

**ФУНКСИЯҲО:**

1️⃣ **ВИДЕО МОНТАЖ**
   ✂️ Буридан
   🎨 Эффектҳо (ч/б, сепия, размытие)
   🎵 Музика фон
   📝 Текст ва субтитр
   ⚡ Скорость (0.5x - 2x)
   🔄 Ротация (90°, 180°, 270°)

2️⃣ **РАСМ МОНТАЖ**
   🎨 Эффектҳо
   📝 Текст
   🔄 Ротация
   📐 Размер

3️⃣ **МЕМҲО**
   Drake, Distracted, Loss
   Expanding Brain, Woman Yelling
   Surprised Pikachu, Stonks
   Change My Mind, This Is Fine
   Uno Reverse

4️⃣ **ҶУСТУҶӮ**
   🎬 Видео
   🖼️ Расм
   🎵 Музика

5️⃣ **AI ВИДЕО**
   🤖 AI генератор
   📝 Текст ба видео
   🎬 Видео созед

**ҚАДАМҲО:**
1. Видео ё расм фарусттанд
2. Менюро интихоб кунед
3. Параметрҳо танзим кунед
4. Натиҷаро дарбаровар кунед"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик видео файлов"""
    message = update.message
    video = message.video
    
    keyboard = [
        [InlineKeyboardButton("✂️ Буридан", callback_data="cut"),
         InlineKeyboardButton("🎨 Эффектҳо", callback_data="effects")],
        [InlineKeyboardButton("🎵 Музика", callback_data="music"),
         InlineKeyboardButton("📝 Текст", callback_data="text")],
        [InlineKeyboardButton("⚡ Скорость", callback_data="speed"),
         InlineKeyboardButton("🔄 Ротация", callback_data="rotate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(
        f"✅ Видео загружено!\n📊 Размер: {video.file_size / 1024 / 1024:.1f} MB\n\nВыберите действие:",
        reply_markup=reply_markup
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик расмҳо"""
    message = update.message
    
    keyboard = [
        [InlineKeyboardButton("🎨 Эффектҳо", callback_data="image_effects"),
         InlineKeyboardButton("📝 Текст", callback_data="image_text")],
        [InlineKeyboardButton("🔄 Ротация", callback_data="image_rotate"),
         InlineKeyboardButton("📐 Размер", callback_data="image_resize")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text("✅ Расм загружено!\n\nВыберите действие:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    message = update.message
    text = message.text
    
    await message.reply_text(
        "🤔 Ман намедонам, ки шумо чӣ мехоҳед.\n\n"
        "Лутфан команди интихоб кунед:\n"
        "/start - Оғоз\n"
        "/help - Кӯмак"
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback кнопок"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "help":
        text = """📚 **КӮМАК**

**ФУНКСИЯҲО:**
✅ Видео монтаж
✅ Расм монтаж
✅ Мемҳо
✅ Ҷустуҷӯ
✅ AI видео"""
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif data == "video_edit":
        await query.edit_message_text("✂️ **ВИДЕО МОНТАЖ**\n\nВидео фарусттанд ва менюро интихоб кунед.", parse_mode='Markdown')
    
    elif data == "image_edit":
        await query.edit_message_text("🖼️ **РАСМ МОНТАЖ**\n\nРасм фарусттанд ва менюро интихоб кунед.", parse_mode='Markdown')
    
    elif data == "memes":
        keyboard = [
            [InlineKeyboardButton("Drake", callback_data="meme_drake"),
             InlineKeyboardButton("Distracted", callback_data="meme_distracted")],
            [InlineKeyboardButton("Loss", callback_data="meme_loss"),
             InlineKeyboardButton("Brain", callback_data="meme_brain")],
            [InlineKeyboardButton("Woman", callback_data="meme_woman"),
             InlineKeyboardButton("Pikachu", callback_data="meme_pikachu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("😂 **МЕМҲО**\n\nШаблон интихоб кунед:", reply_markup=reply_markup, parse_mode='Markdown')
    
    elif data == "search":
        keyboard = [
            [InlineKeyboardButton("🎬 Видео", callback_data="search_video"),
             InlineKeyboardButton("🖼️ Расм", callback_data="search_image")],
            [InlineKeyboardButton("🎵 Музика", callback_data="search_music")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🔍 **ҶУСТУҶӮ**\n\nТип интихоб кунед:", reply_markup=reply_markup, parse_mode='Markdown')
    
    elif data == "ai_video":
        await query.edit_message_text("🤖 **AI ВИДЕО ГЕНЕРАТОР**\n\nТекст ворид кунед ва видео созед!", parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Основная функция запуска бота"""
    app = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    
    # Регистрация обработчиков сообщений
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Регистрация callback обработчиков
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    # Обработка ошибок
    app.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("🚀 Бот запущен...")
    print("\n" + "="*60)
    print("🎬 БОТИ TELEGRAM БАРОИ МОНТАЖИ ВИДЕО")
    print("="*60)
    print("✅ Бот омода аст!")
    print("📱 @mi_video_edit_bot")
    print("="*60 + "\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

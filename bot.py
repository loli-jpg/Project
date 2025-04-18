from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    CallbackContext,
)
from telegram.ext.filters import TEXT, COMMAND
from playlist_manager import PlaylistManager
from utils import search_music
from database import init_db, Session
import os
from dotenv import load_dotenv
import logging

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
init_db()

class MusicBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        
        # Регистрация обработчиков
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('newplaylist', self.new_playlist))
        self.application.add_handler(CommandHandler('myplaylists', self.show_playlists))
        self.application.add_handler(CommandHandler('search', self.search_music))
        self.application.add_handler(CallbackQueryHandler(self.button_click))
        self.application.add_handler(MessageHandler(TEXT & ~COMMAND, self.handle_message))

    async def start(self, update: Update, context: CallbackContext):
        user = update.effective_user
        await update.message.reply_text(
            f"Привет, {user.first_name}! Я музыкальный бот для Яндекс.Музыки.\n\n"
            "Доступные команды:\n"
            "/newplaylist - Создать плейлист\n"
            "/myplaylists - Мои плейлисты\n"
            "/search - Найти музыку\n"
        )

    async def new_playlist(self, update: Update, context: CallbackContext):
        context.user_data['awaiting_playlist_name'] = True
        await update.message.reply_text("Введите название нового плейлиста:")

    async def show_playlists(self, update: Update, context: CallbackContext):
        session = Session()
        try:
            user = PlaylistManager.get_or_create_user(update.effective_user.id)
            playlists = session.query(Playlist).filter_by(user_id=user.id).all()
            
            if not playlists:
                await update.message.reply_text("У вас пока нет плейлистов. Создайте новый с помощью /newplaylist")
                return
            
            keyboard = []
            for playlist in playlists:
                keyboard.append([InlineKeyboardButton(playlist.name, callback_data=f"view_playlist_{playlist.id}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Ваши плейлисты:", reply_markup=reply_markup)
        finally:
            session.close()

    async def search_music(self, update: Update, context: CallbackContext):
        context.user_data['awaiting_search_query'] = True
        await update.message.reply_text("Введите название трека или исполнителя для поиска:")

    async def handle_message(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        text = update.message.text
        session = Session()
        
        try:
            if context.user_data.get('awaiting_playlist_name'):
                del context.user_data['awaiting_playlist_name']
                user = PlaylistManager.get_or_create_user(user_id)
                playlist = PlaylistManager.create_playlist(user.id, text)
                await update.message.reply_text(f"Плейлист '{playlist.name}' создан!")
            
            elif context.user_data.get('awaiting_search_query'):
                del context.user_data['awaiting_search_query']
                try:
                    results = search_music(text)
                    
                    if not results:
                        await update.message.reply_text("Ничего не найдено в Яндекс.Музыке.")
                        return
                    
                    message = "Результаты из Яндекс.Музыки:\n"
                    for i, track in enumerate(results[:5], 1):
                        message += f"{i}. {track['artist']} - {track['title']}\nСсылка: {track['url']}\n\n"
                    await update.message.reply_text(message)
                except Exception as e:
                    logging.error(f"Ошибка поиска: {e}")
                    await update.message.reply_text("Произошла ошибка при поиске. Попробуйте позже.")
        finally:
            session.close()

    async def button_click(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data
        session = Session()
        
        try:
            if data.startswith('view_playlist_'):
                playlist_id = int(data.split('_')[-1])
                playlist = session.query(Playlist).get(playlist_id)
                tracks = session.query(Track).filter_by(playlist_id=playlist_id).all()
                
                if not tracks:
                    await query.edit_message_text(f"Плейлист '{playlist.name}' пуст.")
                    return
                
                message = f"Треки в плейлисте '{playlist.name}':\n\n"
                for i, track in enumerate(tracks, 1):
                    message += f"{i}. {track.artist} - {track.title}\n"
                
                keyboard = [
                    [InlineKeyboardButton("Удалить плейлист", callback_data=f"delete_playlist_{playlist_id}")],
                    [InlineKeyboardButton("Поделиться", callback_data=f"share_playlist_{playlist_id}")],
                    [InlineKeyboardButton("Назад", callback_data="back_to_playlists")]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(message, reply_markup=reply_markup)
            
            elif data == 'back_to_playlists':
                user = PlaylistManager.get_or_create_user(query.from_user.id)
                playlists = session.query(Playlist).filter_by(user_id=user.id).all()
                
                keyboard = []
                for playlist in playlists:
                    keyboard.append([InlineKeyboardButton(playlist.name, callback_data=f"view_playlist_{playlist.id}")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text("Ваши плейлисты:", reply_markup=reply_markup)
            
            elif data.startswith('delete_playlist_'):
                await query.answer("Функция удаления плейлиста будет реализована позже.")
            
            elif data.startswith('share_playlist_'):
                await query.answer("Функция общего доступа будет реализована позже.")
        finally:
            session.close()

    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    token = "7227865213:AAGbkqOdmQCSHli3Oj2vHNC-0nNnkLFi8vA"
    bot = MusicBot(token)
    bot.run()

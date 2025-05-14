import asyncio
import logging
from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)
from dotenv import load_dotenv
import os
import hashlib
from functools import wraps

load_dotenv()

TG_API_KEY = os.getenv('TG_API_KEY', '')
TG_AUTH = os.getenv('TG_AUTH', '')
TG_ADMIN_CHAT_IDS = [int(id.strip()) for id in os.getenv('TG_ADMIN_CHAT_ID', '').split(',') if id.strip().isdigit()]

active_sessions = set()

def auth_ok(func):

    @wraps(func)
    async def wrapped(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    
        if update.effective_chat.id not in active_sessions:
    
            await update.message.reply_text('🔒 Sorry, you need to be ADMIN for this option')
            return
    
        return await func(self, update, context, *args, **kwargs)
    
    return wrapped

class TeleLogs:
    
    def __init__(self, app=None):
    
        self.bot = None
        self.application = None
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._loop = None

    def init_app(self, app):
    
        if not TG_API_KEY:
    
            app.logger.warning('ERROR -> TG API KEY is missing!')
            return

        try:
    
            self.bot = Bot(token=TG_API_KEY)
            self.application = Application.builder().token(TG_API_KEY).build()



            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("auth", self.auth))
            self.application.add_handler(CommandHandler("logs", self.get_logs))
            self.application.add_handler(CommandHandler("status", self.server_status))



            self.setup_logging(app)


        except Exception as e:

            app.logger.error(f'ERROR [TG] -> Conn. error : {str(e)}')



    def start_polling(self):

        self._running = True
        self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._run_polling())


        except Exception as e:

            self.logger.error(f'DEBUG [TG] -> Polling error (network?): {str(e)}')


        finally:

            if self._loop.is_running():

                self._loop.close()



    async def _run_polling(self):

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        while self._running:
    
            await asyncio.sleep(1)

    
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()

    
    def stop(self):

        self._running = False
        
        if self._loop and self._loop.is_running():
        
            self._loop.call_soon_threadsafe(self._loop.stop)

    
    def setup_logging(self, app):
    
        class TelegramLogHandler(logging.Handler):
    
            def __init__(self, bot, application):
                super().__init__()
                self.bot = bot
                self.application = application

            def emit(self, record):
    
                for chat_id in active_sessions:
    
                    try:
    
                        asyncio.run_coroutine_threadsafe(
                            self.bot.send_message(
                                chat_id=chat_id,
                                text=f"📝 {self.format(record)}",
                                parse_mode='Markdown'
                            ),
                            self._loop
                        )
    
    
                    except Exception as e:
    
                        print(f'ERROR [TG] -> Log cannot be sent : {str(e)}')
                        app.logger.error(f'ERROR [TG] -> Log cannot be sent : {str(e)}')

        
        
        telegram_handler = TelegramLogHandler(self.bot, self.application)
        telegram_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        telegram_handler.setFormatter(formatter)
        
        app.logger.addHandler(telegram_handler)


    # COMMANDS
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        is_admin = update.effective_chat.id in TG_ADMIN_CHAT_IDS
        await update.message.reply_text(
            "🤖 **JUST LEARN.ING SERVER BOT**\n"
            "Available commands:\n\n"
            "/auth <password> - Admin login\n"
            "/logs - Check logs\n"
            "/status - Server Status\n"
            f"🔹 User is -> {'ADMIN' if is_admin else 'NON-ADMIN'}"
        )

    async def auth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        if not context.args:
        
            await update.message.reply_text("Usage: /auth <password>")
            return

        input_password = context.args[0]
        input_hash = hashlib.sha256(input_password.encode()).hexdigest()

        if input_hash == TG_AUTH:
        
            print('DEBUG [TgBot] -> Bot Login OK!')
            active_sessions.add(update.effective_chat.id)
        
            await update.message.reply_text('✅ Login OK! Welcome, Alexandr :-D')
        
        else:
        
            print('ERROR [TgBot] -> Bad login attempt.')
            await update.message.reply_text('❌ WRONG PASSWORD!')

    @auth_ok
    
    async def get_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    
        print('DEBUG [TgBot] -> Logs sent!')
        await update.message.reply_text('📜 Last Server Logs ...\n\n')

    
    @auth_ok
    
    async def server_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    
        print('DEBUG [TgBot] -> Server status request sent')
        await update.message.reply_text('🟢 Server is up!')

    
    
    async def notify_admins(self, message):
    
        for admin_id in TG_ADMIN_CHAT_IDS:
    
            try:
    
    
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"📢 Admin Notification:\n\n{message}",
                    parse_mode='Markdown'
                )
    
            except Exception as e:
    
                print(f'ERROR [TgBot] -> Error notifying admin {admin_id}: {str(e)}')
                self.logger.error(f'ERROR [TgBot] -> Error notifying admin {admin_id}: {str(e)}')

telelog = TeleLogs()

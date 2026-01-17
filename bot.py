import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from datetime import datetime
import pytz

# إعدادات السحابة
PORT = int(os.environ.get('PORT', 8080))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.token = os.environ.get('BOT_TOKEN')
        if not self.token:
            raise ValueError("BOT_TOKEN غير موجود في متغيرات البيئة")
        
        self.admin_ids = [int(id.strip()) for id in os.environ.get('ADMIN_IDS', '').split(',') if id.strip()]
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بدء البوت"""
        user = update.effective_user
        
        keyboard = [
            [InlineKeyboardButton("📊 الأسواق العالمية", callback_data='market')],
            [InlineKeyboardButton("📈 التحليلات اليومية", callback_data='analysis')],
            [InlineKeyboardButton("📰 أخبار مالية", callback_data='news')],
            [InlineKeyboardButton("🆘 المساعدة", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
        🏆 **مرحباً {user.first_name} في بوت التداول!**
        
        🤖 **البوت يعمل بنجاح على السحابة**
        📊 **آخر تحديث:** {datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%Y-%m-%d %H:%M')}
        
        **اختر من القائمة:**
        """
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض حالة البوت"""
        status_text = """
        ✅ **حالة البوت:** يعمل بنجاح
        
        🌐 **النظام:** يعمل على السحابة (Render)
        🕒 **آخر تشغيل:** الآن
        📊 **المهام:** جاهزة للاستخدام
        
        **لبدء الاستخدام:**
        /start - عرض القائمة الرئيسية
        /help - المساعدة والأوامر
        """
        await update.message.reply_text(status_text)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الأزرار"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'market':
            await self.market_status(update, context)
        elif query.data == 'analysis':
            await self.daily_analysis(update, context)
        elif query.data == 'news':
            await self.financial_news(update, context)
        elif query.data == 'help':
            await self.help_command(update, context)
    
    async def market_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """حالة الأسواق"""
        market_data = """
        📈 **أسواق الأسهم العالمية:**
        🇺🇸 S&P 500: 4,800 (+0.5%)
        🇺🇸 Nasdaq: 16,900 (+0.8%)
        🇪🇺 Euro Stoxx 50: 4,500 (+0.3%)
        
        💰 **العملات:**
        💵 USD/EUR: 0.92 (-0.1%)
        💵 USD/GBP: 0.79 (+0.2%)
        💵 USD/SAR: 3.75 (ثابت)
        
        🛢️ **السلع:**
        ⚫ النفط: $78.50 (+1.2%)
        🟡 الذهب: $1,950 (+0.5%)
        
        ⏰ آخر تحديث: {time}
        """.format(time=datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%H:%M'))
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=market_data
        )
    
    async def daily_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التحليلات اليومية"""
        analysis = """
        📊 **تحليلات اليوم {date}**
        
        🔹 **الأسهم الأمريكية:**
        - التكنولوجيا: اتجاه صاعد مع نتائج أرباح قوية
        - المالية: مستقرة مع توقعات رفع الفائدة
        
        🔹 **العملات:**
        - الدولار: ضعف مؤقت أمام اليورو
        - الريال: مستقر مع تحسن الاقتصاد
        
        🔹 **التوصيات:**
        1️⃣ مراقبة أسهم التكنولوجيا
        2️⃣ شراء الذهب كتحوط
        3️⃣ تجنب السندات طويلة الأجل
        
        ⚠️ **تنبيه:** هذه آراء تحليلية وليست توصيات استثمارية
        """.format(date=datetime.now().strftime('%Y-%m-%d'))
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=analysis
        )
    
    async def financial_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """الأخبار المالية"""
        news = """
        📰 **آخر الأخبار المالية**
        
        1️⃣ **البنوك المركزية:**
        - الفيدرالي الأمريكي: تأجيل خفض الفائدة
        - البنك المركزي الأوروبي: تثبيت السياسة
        
        2️⃣ **الشركات:**
        - أبل: نتائج أرباح قياسية
        - تيسلا: نمو المبيعات بنسبة 15%
        
        3️⃣ **الاقتصاد العالمي:**
        - نمو الناتج المحلي الأمريكي 3.2%
        - انخفاض التضخم في أوروبا
        
        🔗 **مصادر موثوقة:**
        - Bloomberg
        - Reuters
        - CNBC Arabia
        """
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=news
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """الأوامر المتاحة"""
        help_text = """
        🆘 **أوامر البوت:**
        
        /start - بدء البوت والقائمة
        /status - حالة البوت
        /market - أسعار الأسواق
        /analysis - التحليلات اليومية
        /news - الأخبار المالية
        /help - هذه الرسالة
        
        📞 **للتواصل مع المطور:**
        @YourUsername
        
        ⚠️ **تذكير:** 
        - البوت لأغراض تعليمية
        - التحليلات آراء شخصية
        - لا تنسى التحليل الشخصي
        """
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=help_text
        )
    
    def setup_handlers(self, application):
        """إعداد Handlers"""
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("status", self.status))
        application.add_handler(CommandHandler("market", self.market_status))
        application.add_handler(CommandHandler("analysis", self.daily_analysis))
        application.add_handler(CommandHandler("news", self.financial_news))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CallbackQueryHandler(self.button_handler))
    
    async def run_webhook(self):
        """تشغيل Webhook للسحابة"""
        application = Application.builder().token(self.token).build()
        self.setup_handlers(application)
        
        if WEBHOOK_URL:
            # وضع Webhook للسحابة
            await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{self.token}")
            await application.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                webhook_url=f"{WEBHOOK_URL}/{self.token}"
            )
        else:
            # وضع Polling للتطوير المحلي
            await application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def run_polling(self):
        """تشغيل Polling"""
        application = Application.builder().token(self.token).build()
        self.setup_handlers(application)
        application.run_polling(allowed_updates=Update.ALL_TYPES)

async def main():
    """الدالة الرئيسية"""
    bot = TradingBot()
    await bot.run_webhook()

if __name__ == '__main__':
    # للتشغيل المحلي
    if os.environ.get('RENDER', '').lower() == 'true':
        asyncio.run(main())
    else:
        bot = TradingBot()
        bot.run_polling()
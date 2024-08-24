import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta, timezone
import re




bot = telebot.TeleBot('TOKEN_here')

def parse_duration(duration_str):
    """ Parse duration string and return a timedelta object. """
    match = re.match(r'(\d+)([smhd])', duration_str)
    if not match:
        return None
    
    value, unit = match.groups()
    value = int(value)
    
    if unit == 's':  
        return timedelta(seconds=value)
    elif unit == 'm': 
        return timedelta(minutes=value)
    elif unit == 'h':  
        return timedelta(hours=value)
    elif unit == 'd': 
        return timedelta(days=value)
    
    return None



   
@bot.message_handler(commands=['limit'])
def restrict_user(message):
      
        args = message.text.split()
        if len(args) < 2:
            bot.send_message(message.chat.id, "لطفاً مدت زمان را مشخص کنید. مثال: `/limit 10m`")
            return
        
        duration_str = args[1]
        duration = parse_duration(duration_str)
        
        if not duration:
            bot.send_message(message.chat.id, "مدت زمان نامعتبر است. لطفاً از فرمت‌های معتبر مانند `10s`, `5m`, `1d` استفاده کنید.")
            return

        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            until_date = datetime.now(timezone.utc) + duration
            try:
                bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    until_date=until_date,
                    can_send_messages=False,  
                    can_send_media_messages=False, 
                    can_send_other_messages=False,  
                    can_add_web_page_previews=False  
                )
                bot.send_message(message.chat.id, "دسترسی کاربر محدود شد.")
            except Exception as e:
                print("Oops")
                bot.send_message(message.chat.id, e)
                
        else:
            bot.send_message(message.chat.id, "لطفاً پیامی که می‌خواهید به آن پاسخ دهید را انتخاب کنید.")

@bot.message_handler(commands=['ban'])
def send_glasses_menu(message):
    if message.chat.type in ['group', 'supergroup']:
           
            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                replied_user = message.reply_to_message.from_user
                full_name = f"{replied_user.first_name} {replied_user.last_name}" if replied_user.last_name else replied_user.first_name
               
                bot.kick_chat_member(message.chat.id, user_id)
                bot.send_message(message.chat.id, f"کاربر به نام {full_name} از گروه حذف شد")
            else:
                bot.send_message(message.chat.id, "لطفاً پیامی که می‌خواهید به آن پاسخ دهید را انتخاب کنید.")
    else:
            bot.send_message(message.chat.id, "این دستور فقط در گروه‌ها قابل استفاده است.")

@bot.message_handler(commands=['help'])
def send_glasses_menu(message):
    markup = InlineKeyboardMarkup()

  
    markup.add(InlineKeyboardButton("اضافه کردن به گروه", callback_data="AddtoGroup"))
    markup.add(InlineKeyboardButton("راهنما مدیریت گروه", callback_data="HelpCommand"))

    bot.send_message(message.chat.id, "چه نوع راهنمایی میخواهید دریافت کنید؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "AddtoGroup":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("راهنما مدیریت گروه", callback_data="HelpCommand"))
       
        bot.edit_message_text("""
                         📦 مراحل راه‌اندازی:

روی لینک زیر کلیک کنید و گروه مورد نظر خود را انتخاب کنید:
[اینجا کلیک کنید](https://t.me/GroupBaanBot?startgroup=new)

بعد از اضافه کردن به گروه، لطفاً اون رو ادمین کنید\\.


🔹 @GroupBaanBot

                         """,call.message.chat.id, message_id=call.message.message_id,parse_mode="MarkdownV2", disable_web_page_preview=True,reply_markup=markup)
        
        
    elif call.data == "HelpCommand":
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("اضافه کردن به گروه", callback_data="AddtoGroup"))
       
                bot.edit_message_text("""دستورات عمومی:

/start
شروع و فعال‌سازی ربات در گروه

/help
دریافت لیست دستورات و راهنمای استفاده از ربات

/settings
دسترسی به تنظیمات گروه و ربات

دستورات مدیریتی:

/ban 
نامکاربر
/
آیدی
نامکاربر/آیدی
مسدود کردن 
بن
بن یک کاربر از گروه

/unban 
نامکاربر
/
آیدی
نامکاربر/آیدی
رفع مسدودیت 
آنبن
آنبن یک کاربر

/mute 
نامکاربر
/
آیدی
نامکاربر/آیدی 
مدت‌زمان
مدت‌زمان
بی‌صدا کردن 
میوت
میوت یک کاربر برای مدت‌زمان مشخص

/unmute 
نامکاربر
/
آیدی
نامکاربر/آیدی
برداشتن حالت بی‌صدا از یک کاربر

/warn 
نامکاربر
/
آیدی
نامکاربر/آیدی
اخطار دادن به یک کاربر 
باقابلیتتنظیمتعداداخطارهاقبلازمسدودیت
باقابلیتتنظیمتعداداخطارهاقبلازمسدودیت

/kick 
نامکاربر
/
آیدی
نامکاربر/آیدی
اخراج کردن یک کاربر از گروه

/pin 
پیام
/
پست
پیام/پست
سنجاق کردن 
پین
پین یک پیام در گروه

/unpin
برداشتن سنجاق از پیام فعلی

دستورات امنیتی:

/lock 
لینک
/
تصاویر
/
ویدیوها
/
گیف‌ها
لینک/تصاویر/ویدیوها/گیف‌ها
قفل کردن ارسال انواع محتوا در گروه

/unlock 
لینک
/
تصاویر
/
ویدیوها
/
گیف‌ها
لینک/تصاویر/ویدیوها/گیف‌ها
باز کردن قفل ارسال محتوا در گروه

/setrules
تنظیم قوانین گروه برای اطلاع‌رسانی به کاربران جدید

/rules
نمایش قوانین گروه برای همه کاربران

🔹 @GroupBaanBot

                         """,call.message.chat.id, message_id=call.message.message_id,parse_mode="MarkdownV2", disable_web_page_preview=True,reply_markup=markup)
        
        


def edit_message(message):
    bot.edit_message_text("This message has been edited!", chat_id=message.chat.id, message_id=message.message_id)

bot.polling()

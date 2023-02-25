import telebot

API_KEY = "6139877305:AAGW3zvvvwrsQgOP0xtCR05qsWpcgqQr4vA"
bot = telebot.TeleBot(API_KEY)

def group_only(func):
    def wrapper(message):
        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            return func(message)
    return wrapper

@group_only
def process_message(message):

    banned_words = ["كس","كسختك","بكسختك","كسخواتكم","بكسخواتكم","كسمك","بكسمك","كسمكم","بكسمكم","الكحبه","الكحبة","القحبة","القحبه","لكحبه","لكحبة","كحاب","قحاب","قحبة","قحبه","كحبة","ابنلحبكه","ابنلكحبة","تبادل مقاطع","زب","زبي","العيورة","العيوره","لعيورة","لعيوره","عيورة","عيوره","شرموطة","شرموطه","الشرموطة","الشرموطه","نياجة","نياجه","تنيج","انيج","أنيج","انيجمك","أنيجمك","عيوشه","عيوشة","أمك عائشة","أمك عائشه","امك عائشة","امك عائشه","يابن عائشه","يابن عائشة","عائشه تنيج","ألعن عائشة","ألعن عائشه","العن عائشة","العن عائشه","عائشة الزانية","عائشه الزانيه","عائشة لزانية","عائشه لزانيه","عائشة زانية","عائشه زانيه","عائشه الطائشه","عائشة الطائشة","صدر عائشة","صدر عائشه","امكم عائشة","أمكم عائشه","في رواياتكم عائشة","في رواياتكم عائشه","برواياتكم عائشة","برواياتكم عائشه","عير بعائشة","عير بعائشه","أنعل عائشة","أنعل عائشه","انعل عائشة","انعل عائشه","إرضاع الكبير","ارضاع الكبير","إرضاع الرجال","ارضاع الرجال","مرضعه الرجال","مرضعة الرجال","لطيزي","طيزك","بطيز","طيز","ألعن عمر","العن عمر","ألعن أبو بكر","العن ابو بكر","لعن الله عمر","لعن الله ابو بكر","لعن الله أبو بكر","أنعل عمر","انعل عمر","أنعل أبو بكر","انعل ابو بكر","الكوادة","الكواده","لكوادة","لكواده","كواويد","كواده","كوادة","كواد","إحنة شيعت علي","إحنه شيعت علي","احنة شيعت علي","احنه شيعت علي","إحنة شيعة علي","إحنه شيعه علي","احنة شيعة علي","احنه شيعه علي","أخواتكم ينيجون","أخواتكم ينيجن","اخواتكم ينيجون","اخواتكم ينيجن","خواتكم ينيجون","خواتكم ينيجن","أبناء المسيار","ابناء المسيار","ابن المسيار","أبناء جهاد النكاح","ابناء جهاد النكاح","ابن جهاد النكاح","ابن زواج المسيار","صعسلم","عير بسنة","عير بسنه","عير بالسنة","عير بالسنه","عير بلسنه","سكس","نيك","عير بعمر","عير بيكم","عير بيك","مناويج","منايك","عيوش","عيربلسنة","عيربلسنه","العير","صلعسلم"]

    admin_ids = ["5569213514"]
    
    banned_word = None
    for word in message.text.split():
        if word in banned_words:
            banned_word = word
            break

    banned = False
    for word in message.text.split():
        if word in banned_words:
            banned = True
            break
    
    if banned:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=0, can_send_messages=False)
            user_mention = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
            bot.send_message(message.chat.id, f"It seems that the user {user_mention} has behaved like Shiites. The bot successfully punished him by muting his account and deleting his message.", parse_mode='HTML')
            
            for admin_id in admin_ids:
                bot.send_message(admin_id, f"The banned word used by the user {user_mention} in chat is: {banned_word}", parse_mode='HTML')

        except telebot.apihelper.ApiException as e:
            print(e)
            bot.send_message(message.chat.id, "Sorry, something went wrong.")
            
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_all_messages(message):
    process_message(message)

@bot.message_handler(commands=['activate'])
@group_only
def start_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ['creator', 'administrator']:
        bot.reply_to(message, "Bot is activated and working successfully.")

bot.polling()
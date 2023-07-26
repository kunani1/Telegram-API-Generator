import json
import requests
from lxml import html
from fake_useragent import FakeUserAgent
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

fake_useragent = FakeUserAgent()

class TelegramApplication:
    def __init__(self, bot_token: str, app_platform: str = "desktop"):
        self.bot_token = bot_token
        self.app_platform = app_platform
        self.random_hash = None
        self.stel_token = None
        self.useragent = fake_useragent.random
    
    def send_password(self, phone_number: str) -> bool:
        try:
            response = requests.post(
                url="https://my.telegram.org/auth/send_password",
                data="phone={0}".format(phone_number),
                headers={
                    "Origin": "https://my.telegram.org",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Reffer": "https://my.telegram.org/auth",
                    "X-Requested-With": "XMLHttpRequest",
                    "Connection": "keep-alive",
                    "Dnt": "1"
                })
            
            get_json = json.loads(response.content)
            self.random_hash = get_json["random_hash"]
            return True
        except:
            return False

    def auth_login(self, phone_number: str, cloud_password: str) -> bool:
        try:
            responses = requests.post(
                url="https://my.telegram.org/auth/login",
                data="phone={0}&random_hash={1}&password={2}".format(phone_number, self.random_hash, cloud_password),
                headers={
                    "Origin": "https://my.telegram.org",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "User-Agent": self.useragent,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Reffer": "https://my.telegram.org/auth",
                    "X-Requested-With": "XMLHttpRequest",
                    "Connection": "keep-alive",
                    "Dnt": "1"
                }
            )
            self.stel_token = responses.cookies['stel_token']
            return True
        except:
            return False

    def auth_app(self) -> tuple:
        try:
            resp = requests.get(
                url="https://my.telegram.org/apps",
                headers={
                    "Cookie": "stel_token={0}".format(self.stel_token),
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": self.useragent,
                    "Reffer": "https://my.telegram.org/org",
                    "Cache-Control": "max-age=0",
                    "Dnt": "1"
                }
            )
            tree = html.fromstring(resp.content)
            api = tree.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
            return api[0], api[1]
        except:
            try:
                s = resp.text.split('"/>')[0]
                value = s.split('<input type="hidden" name="hash" value="')[1]
                
                requests.post(
                    url="https://my.telegram.org/apps/create",
                    data="hash={0}&app_title={1}&app_shortname={2}&app_url={3}&app_platform={4}&app_desc={5}".format(value, self.app_title, self.app_shortname, self.app_url, self.app_platform, self.app_desc),
                    headers={
                        "Cookie": "stel_token={0}".format(self.stel_token),
                        "Origin": "https://my.telegram.org",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                        "User-Agent": self.useragent,
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Accept": "*/*",
                        "Referer": "https://my.telegram.org/apps",
                        "X-Requested-With": "XMLHttpRequest",
                        "Connection": "keep-alive",
                        "Dnt": "1"
                    }
                )
                
                response = requests.get(
                    url="https://my.telegram.org/apps",
                    headers={
                        "Cookie": "stel_token={0}".format(self.stel_token),
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": self.useragent,
                        "Reffer": "https://my.telegram.org/org",
                        "Cache-Control": "max-age=0",
                        "Dnt": "1"
                    }
                )
                trees = html.fromstring(response.content)
                api = trees.xpath('//span[@class="form-control input-xlarge uneditable-input"]//text()')
                return api[0], api[1]
            except:
                return False

# Replace "YOUR_BOT_TOKEN" with the token you obtained from the BotFather on Telegram.
bot_token = "1799299844:AAHXWUfImCIP3FRC6DDYB_41xCjAOkZHo-k"
telegram_app = TelegramApplication(bot_token)

# Define a command handler for the /start command.
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}! I am your Telegram Application bot. "
        fr"Please use the /sendpassword and /authlogin commands to interact with the Telegram application."
    )

# Define a command handler for the /sendpassword command.
def send_password(update: Update, context: CallbackContext):
    user_phone = update.message.text.split()[1]
    if telegram_app.send_password(user_phone):
        update.message.reply_text("Password sent successfully! Use /authlogin command to authenticate.")
    else:
        update.message.reply_text("Failed to send the password. Please try again.")

# Define a command handler for the /authlogin command.
def auth_login(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) != 3:
        update.message.reply_text("Invalid usage. Please use /authlogin <phone_number
            

from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, ClientError, LoginRequired
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Configuration
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
OWNER_USERNAME = "owner_username_here"  # Your Instagram username

# Fun responses
FUN_REPLIES = [
    "Oye {user}, jyada bak bak na kar warna teri juban kat dunga!",
    "Arre {user}, itna bhi serious na ho yaar!",
    "{user} bhai thoda chill kar!",
    "Hahaha... {user} tum to bade funny ho!",
    "{user}, ye kaisi baatein kar rahe ho?",
    "Shhhh {user}... chup raho thodi der!",
    "{user} tum to harami nikle! 😂",
    "Arey {user} bhai, maze le rahe ho kya?",
    "{user} tumse na ho payega!",
    "{user} thodi izzat karo humari!",
]

class InstagramGroupBot:
    def __init__(self):
        self.client = Client()
        self.fun_mode = True
        self.custom_replies = []
        self.active_groups = set()
        
        # Client configuration
        self.client.delay_range = [2, 5]  # More realistic delays
        self.client.set_proxy(None)  # Remove if using proxy
        self.client.set_locale("en_US")
        self.client.set_country("IN")
        self.client.set_timezone_offset(19800)  # 5:30 hours
        
    def login(self):
        try:
            # Try to load previous session
            self.client.load_settings("session.json")
            login_result = self.client.login(USERNAME, PASSWORD)
            
            if not login_result:
                logger.info("Session invalid, logging in fresh...")
                self.client = Client()  # Reset client
                login_result = self.client.login(USERNAME, PASSWORD)
                
            logger.info("Logged in successfully!")
            self.client.dump_settings("session.json")
            return True
            
        except ChallengeRequired as e:
            logger.warning(f"Challenge required: {e}")
            self.handle_challenge()
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def handle_challenge(self):
        try:
            challenge_info = self.client.last_json.get('challenge', {})
            challenge_url = challenge_info.get('url', '')
            
            if challenge_url:
                logger.info(f"Challenge URL: {challenge_url}")
                
                # For email challenge
                if 'email' in challenge_url:
                    code = input("Enter the 6-digit code sent to your email: ")
                    self.client.challenge_resolve(code)
                    logger.info("Challenge resolved successfully!")
                    self.client.dump_settings("session.json")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to handle challenge: {e}")
            return False
    
    def process_all_groups(self):
        try:
            threads = self.client.direct_threads()
            
            for thread in threads:
                if len(thread.users) > 1:  # Only group chats
                    self.active_groups.add(thread.id)
                    
                    for item in thread.items:
                        try:
                            if item.user_id != self.client.user_id:
                                user_info = self.client.user_info(item.user_id)
                                username = user_info.username
                                
                                # Handle owner commands
                                if username.lower() == OWNER_USERNAME.lower() and item.text.startswith("!"):
                                    self.handle_owner_command(thread.id, item.text)
                                    continue
                                    
                                # Send random reply
                                if self.fun_mode and random.random() > 0.7:
                                    reply = random.choice(FUN_REPLIES).format(user=username)
                                    self.client.direct_send(reply, thread_ids=[thread.id])
                                    time.sleep(random.randint(1, 3))  # Random delay
                                    
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                            continue
                            
        except LoginRequired:
            logger.warning("Session expired, re-logging in...")
            self.login()
        except Exception as e:
            logger.error(f"Error processing groups: {e}")
    
    def handle_owner_command(self, thread_id, command):
        try:
            if command == "!help":
                help_text = "Available Commands:\n!info - Bot info\n!fun on/off - Toggle fun mode"
                self.client.direct_send(help_text, thread_ids=[thread_id])
                
            elif command == "!info":
                info = f"Group Bot v2.0\nActive in {len(self.active_groups)} groups"
                self.client.direct_send(info, thread_ids=[thread_id])
                
            elif command == "!fun on":
                self.fun_mode = True
                self.client.direct_send("Fun mode activated!", thread_ids=[thread_id])
                
            elif command == "!fun off":
                self.fun_mode = False
                self.client.direct_send("Fun mode deactivated!", thread_ids=[thread_id])
                
        except Exception as e:
            logger.error(f"Error handling command: {e}")
    
    def run(self):
        if not self.login():
            logger.error("Failed to login, exiting...")
            return
            
        logger.info("Bot started. Listening in all groups...")
        
        while True:
            try:
                self.process_all_groups()
                time.sleep(15)  # Check every 15 seconds
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    bot = InstagramGroupBot()
    bot.run()

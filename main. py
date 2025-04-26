from instagrapi import Client
import random
import time

# Bot Configuration
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"
OWNER_USERNAME = "owner_username_here"  # Bot owner's username

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

# Owner commands
OWNER_COMMANDS = {
    "!info": "Bot information",
    "!help": "Show all commands",
    "!active": "Check bot status",
    "!fun on": "Enable fun mode",
    "!fun off": "Disable fun mode",
    "!addreply": "Add custom reply",
}

class InstagramAutoBot:
    def __init__(self):
        self.client = Client()
        self.fun_mode = True
        self.custom_replies = []
        self.active_groups = set()  # Track groups where bot is active
        
    def login(self):
        try:
            self.client.login(USERNAME, PASSWORD)
            print("Logged in successfully!")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def process_all_groups(self):
        threads = self.client.direct_threads()
        
        for thread in threads:
            # Only process group chats (not 1:1 chats)
            if len(thread.users) > 1:
                self.active_groups.add(thread.id)  # Mark group as active
                
                for item in thread.items:
                    if item.user_id != self.client.user_id:  # Don't reply to self
                        user_info = self.client.user_info(item.user_id)
                        username = user_info.username
                        
                        # Handle owner commands
                        if username.lower() == OWNER_USERNAME.lower() and item.text.startswith("!"):
                            self.handle_owner_command(thread.id, item.text)
                            continue
                            
                        # Send fun reply
                        if self.fun_mode and random.random() > 0.7:  # 70% chance to reply
                            reply = random.choice(FUN_REPLIES + self.custom_replies).format(user=username)
                            self.client.direct_send(reply, thread_ids=[thread.id])
    
    def handle_owner_command(self, thread_id, command):
        if command == "!help":
            help_text = "Owner Commands:\n" + "\n".join([f"{cmd} - {desc}" for cmd, desc in OWNER_COMMANDS.items()])
            self.client.direct_send(help_text, thread_ids=[thread_id])
        
        elif command == "!info":
            info = f"Auto Fun Bot v2.0\nOwner: {OWNER_USERNAME}\nFun Mode: {'ON' if self.fun_mode else 'OFF'}\nActive in {len(self.active_groups)} groups"
            self.client.direct_send(info, thread_ids=[thread_id])
        
        elif command == "!active":
            self.client.direct_send("Bot is active and running in all groups!", thread_ids=[thread_id])
        
        elif command == "!fun on":
            self.fun_mode = True
            self.client.direct_send("Fun mode activated in all groups!", thread_ids=[thread_id])
        
        elif command == "!fun off":
            self.fun_mode = False
            self.client.direct_send("Fun mode deactivated in all groups!", thread_ids=[thread_id])
        
        elif command.startswith("!addreply "):
            new_reply = command[10:]
            self.custom_replies.append(new_reply)
            self.client.direct_send(f"Added new reply: {new_reply}", thread_ids=[thread_id])
    
    def run(self):
        if not self.login():
            return
        
        print("Bot started. Listening in ALL groups...")
        
        while True:
            try:
                self.process_all_groups()
                time.sleep(10)  # Check every 10 seconds
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    bot = InstagramAutoBot()
    bot.run()

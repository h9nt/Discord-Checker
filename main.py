from requests       import Session
from threading      import Thread
from colorama       import Fore, init
from os             import system
from datetime       import datetime


init(autoreset=True)
system('cls')

# Remember its not double check like banned etc.
# U should use proxys btw for bulk checks

class Discord:
    def __init__(self, username, send_to_telegram: bool):
        self.username = username
        self.session = Session()
        self.send_tele = send_to_telegram
        self.chat_id = ""
        self.bot_token = ""
        self.api_url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
        self.headers: dict[str, str] = dict({
            "Content-Type": "application/json",
            "User-Agent": "Discord-Android/194017;RNA"
        })

    def telegram(self, message, token, chat_id):
        return self.session.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": message})
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.BLUE}[{timestamp}]{Fore.RESET} {Fore.CYAN} {message} {Fore.RESET}")

    def check(self):
        try:
            data = {"username": self.username}
            response = self.session.post(self.api_url, headers=self.headers, json=data)
            if 'taken' in response.json() and response.json()['taken'] != False:
                if self.send_tele:
                    self.telegram(f"{self.username} taken", self.bot_token, self.chat_id)
                self.log_message(f"{username} taken")
            elif 'message' in response.json() and response.json()['message'] == "The resource is being rate limited.":
                if self.send_tele:
                    self.telegram(f"{self.username} rate limited", self.bot_token, self.chat_id)
                self.log_message(f"rate limited, try again with proxies")
            else:
                if self.send_tele:
                    self.telegram(f"{self.username} available", self.bot_token, self.chat_id)
                self.log_message(f"{username} available")
        except Exception as e:
            if self.send_tele:
                self.telegram(f"Error: {e}", self.bot_token, self.chat_id)
            self.log_message(f"Error: {e}")
    
    def main(self):
        Thread(target=self.check).start()


if __name__ == "__main__":
    combo = input("\n Combo >>> ")
    username = open(combo, "r").read().splitlines()
    for user in username:
        Discord(user, False).main()

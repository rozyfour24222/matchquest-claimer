import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import random
import json
from urllib.parse import parse_qs

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data-proxy.json")
config_file = os.path.join(script_dir, "config.json")


class MatchQuest:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}MatchQuest Auto Claimer
        t.me/smartairdrop2120
        
        """

        self.parse_data = lambda data: {
            key: value[0] for key, value in parse_qs(data).items()
        }

        self.autogame = (
            json.load(open(config_file, "r")).get("autogame", "false").lower() == "true"
        )

    def headers(self):
        return {
            "host": "tgapp-api.matchain.io",
            "connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://tgapp.matchain.io",
            "x-requested-with": "tw.nekomimi.nekogram",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://tgapp.matchain.io/",
            "accept-language": "en,en-US;q=0.9",
        }

    def proxies(self, proxy_info):
        return {"http": f"{proxy_info}"}

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def login(self, data, proxy_info):
        parser = self.parse_data(data)
        user = json.loads(parser["user"])
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/login"
        headers = self.headers()
        payload = json.dumps(
            {
                "uid": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "username": user["username"],
                "tg_login_params": data,
            }
        )
        proxies = self.proxies(proxy_info=proxy_info)
        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def get_balance(self, token, user_id, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/balance"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})
        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def get_reward(self, token, user_id, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})
        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def farming(self, token, user_id, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})
        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def claim(self, token, user_id, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})
        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def invite_claim(self, token, user_id, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})
        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def play_game(self, token, proxy_info):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"
        headers = self.headers()
        headers["authorization"] = token
        proxies = self.proxies(proxy_info=proxy_info)

        while True:
            response = requests.get(url=url, headers=headers, proxies=proxies)
            game_id = response.json()["data"]["game_id"]
            game_count = response.json()["data"]["game_count"]
            if response.status_code != 200:
                self.log(f"{red}Something went wrong. Please try to re-run!")
                return False
            if game_id != "":
                try:
                    self.log(f"{yellow}Playing game...")
                    time.sleep(30)
                    point = random.randint(50, 100)
                    payload = json.dumps({"game_id": game_id, "point": point})
                    url_claim = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
                    res_game = requests.post(
                        url=url_claim, headers=headers, data=payload, proxies=proxies
                    )
                    if res_game.status_code != 200:
                        self.log(f"{red}Play game failure!")
                        continue

                    self.log(f"{green}Play game successful, earned {white}{point}")
                    self.log(f"{green}Game left: {white}{game_count}")
                    if game_count <= 0:
                        self.log(f"{yellow}Run out of ticket!")
                        return False
                except:
                    self.log(f"{red}Play game error!")
                    return False
            else:
                self.log(f"{yellow}No game ticket to play!")
                return False

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def parse_proxy_info(self, proxy_info):
        try:
            stripped_url = proxy_info.split("://", 1)[-1]
            credentials, endpoint = stripped_url.split("@", 1)
            user_name, password = credentials.split(":", 1)
            ip, port = endpoint.split(":", 1)
            return {"user_name": user_name, "pass": password, "ip": ip, "port": port}
        except:
            return None

    def main(self):
        self.clear_terminal()
        print(self.banner)
        accounts = json.load(open(data_file, "r"))["accounts"]
        num_acc = len(accounts)
        self.log(self.line)
        self.log(f"{green}Numer of account: {white}{num_acc}")
        while True:
            end_at_list = []
            for no, account in enumerate(accounts):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = self.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    self.log(
                        f"{red}Check proxy format: {white}http://user:pass@ip:port"
                    )
                    break
                ip_adress = parsed_proxy_info["ip"]
                self.log(f"{green}IP Address: {white}{ip_adress}")

                # Login
                try:
                    self.log(f"{yellow}Getting user information...")
                    login = self.login(data=data, proxy_info=proxy_info).json()
                    token = login["data"]["token"]
                    user_id = login["data"]["user"]["uid"]
                    first_name = login["data"]["user"]["first_name"]
                    user_name = login["data"]["user"]["username"]
                    invite_limit = login["data"]["user"]["invite_limit"]
                    self.log(
                        f"{green}User info: {white}{first_name} ({user_name} - {user_id})"
                    )
                    self.log(f"{green}Invite limit: {white}{invite_limit}")

                    # Balance
                    try:
                        get_balance = self.get_balance(
                            token=token, user_id=user_id, proxy_info=proxy_info
                        ).json()
                        balance = get_balance["data"]
                        self.log(f"{green}Balance: {white}{balance / 1000}")
                    except Exception as e:
                        self.log(f"{red}Get balance error!!!")

                    # Reward
                    try:
                        get_reward = self.get_reward(
                            token=token, user_id=user_id, proxy_info=proxy_info
                        ).json()
                        end_at = (
                            float(get_reward["data"]["next_claim_timestamp"]) / 1000
                        )
                        readable_time = datetime.fromtimestamp(end_at).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        self.log(f"{green}Farm end at: {white}{readable_time}")
                        end_at_list.append(end_at)
                    except Exception as e:
                        self.log(f"{red}Get reward error!!!")

                    # Claim from ref
                    try:
                        self.log(f"{yellow}Trying to claim from ref...")
                        invite_claim = self.invite_claim(
                            token=token, user_id=user_id, proxy_info=proxy_info
                        ).json()
                        claim_from_ref = int(invite_claim["data"])
                        if claim_from_ref != 0:
                            self.log(
                                f"{green}Claim from ref: {white}{claim_from_ref / 1000}"
                            )
                        else:
                            self.log(f"{yellow}No point from ref!")
                    except Exception as e:
                        self.log(f"{red}Claim from ref error!!!")

                    # Claim
                    try:
                        self.log(f"{yellow}Trying to claim...")
                        claim = self.claim(
                            token=token, user_id=user_id, proxy_info=proxy_info
                        )

                        if claim.status_code == 200:
                            self.log(f"{green}Claim successful!")
                            # Balance
                            try:
                                get_balance = self.get_balance(
                                    token=token, user_id=user_id, proxy_info=proxy_info
                                ).json()
                                balance = get_balance["data"]
                                self.log(
                                    f"{green}Balance after Claim: {white}{balance / 1000}"
                                )
                            except Exception as e:
                                self.log(f"{red}Get balance error!!!")

                            # Farming
                            try:
                                self.log(f"{yellow}Trying to farm...")
                                farming = self.farming(
                                    token=token, user_id=user_id, proxy_info=proxy_info
                                )
                                if farming.status_code == 200:
                                    self.log(f"{green}Farm successful!")
                                else:
                                    self.log(f"{yellow}Not time to farm yet!")
                            except Exception as e:
                                self.log(f"{red}Farming error!!!")
                        else:
                            self.log(f"{yellow}Not time to claim yet!")
                    except Exception as e:
                        self.log(f"{red}Claim error!!!")

                    # Play game
                    if self.autogame:
                        self.play_game(token=token, proxy_info=proxy_info)
                        # Balance
                        try:
                            get_balance = self.get_balance(
                                token=token, user_id=user_id, proxy_info=proxy_info
                            ).json()
                            balance = get_balance["data"]
                            self.log(f"{green}Current balance: {white}{balance / 1000}")
                        except Exception as e:
                            self.log(f"{red}Get balance error!!!")

                except Exception as e:
                    self.log(f"{red}Login error!!!")
                    print(2)

            print()
            # Wait time
            if end_at_list:
                now = datetime.now().timestamp()
                wait_times = [end_at - now for end_at in end_at_list if end_at > now]
                if wait_times:
                    wait_time = min(wait_times)
                else:
                    wait_time = 15 * 60
            else:
                wait_time = 15 * 60

            wait_hours = int(wait_time // 3600)
            wait_minutes = int((wait_time % 3600) // 60)
            wait_seconds = int(wait_time % 60)

            wait_message_parts = []
            if wait_hours > 0:
                wait_message_parts.append(f"{wait_hours} hours")
            if wait_minutes > 0:
                wait_message_parts.append(f"{wait_minutes} minutes")
            if wait_seconds > 0:
                wait_message_parts.append(f"{wait_seconds} seconds")

            wait_message = ", ".join(wait_message_parts)
            self.log(f"{yellow}Wait for {wait_message}!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        match_quest = MatchQuest()
        match_quest.main()
    except KeyboardInterrupt:
        sys.exit()

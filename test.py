INITIAL_PRICE = 1
INITIAL_SUPPLY = 1000000000
F = 0.5


class User:
    def __init__(self):
        self.user_gold = 0
        self.user_silver = 1000


class Bancor:
    def __init__(self, collateral, token_supply):
        self.collateral = collateral
        self.token_supply = token_supply

    def buy_tokens(self, reserve_deposit):
        new_token_supply = self.token_supply * (
            (1 + reserve_deposit / self.reserve_balance) ** (1 / self.reserve_ratio) - 1
        )
        self.token_supply += new_token_supply
        self.reserve_balance += reserve_deposit
        return new_token_supply

    def sell_tokens(self, tokens_sold):
        reserve_received = self.reserve_balance * (
            1 - (1 - tokens_sold / self.token_supply) ** self.reserve_ratio
        )
        self.token_supply -= tokens_sold
        self.reserve_balance -= reserve_received
        return reserve_received


def buy_token(user: User, gold_amount, bancor: Bancor):
    silver_amount = gold_amount / bancor.price()
    if silver_amount > user.user_silver:
        print("Not Enought silver")
        return
    user.user_silver -= silver_amount
    user.user_gold += gold_amount
    bancor.buy_tokens(silver_amount)


def sell_token(user: User, gold_amount, bancor: Bancor):
    if user.user_gold < gold_amount:
        print("Not Enought gold")
        return
    user.user_gold -= gold_amount
    user.user_silver += gold_amount * bancor.price()
    bancor.sell_tokens(gold_amount)


BANCOR = Bancor(INITIAL_SUPPLY, INITIAL_SUPPLY, F)
USER = User()
USER2 = User()

while True:
    print(
        "Use commans /s {float} - for sale, /b {float} - buy /u - to get user info, /gold - to get gold info /change_user"
    )
    command = input("->>")
    current_user = USER

    if command.startswith("/s"):
        gold = float(command.split(" ")[1])
        sell_token(current_user, gold, BANCOR)
    elif command.startswith("/b"):
        gold = float(command.split(" ")[1])
        buy_token(current_user, gold, BANCOR)
    elif command.startswith("/u"):
        print(current_user.__dict__)
    elif command.startswith("/gold"):
        d = BANCOR.__dict__.copy()
        d.update({"price": BANCOR.price()})
        print(d)
    elif command.startswith("/change_user"):
        if current_user == USER:
            current_user = USER2
            print("USER1 -> USER2")
        else:
            current_user = USER
            print("USER2 -> USER1")

    else:
        print("Undefined command")

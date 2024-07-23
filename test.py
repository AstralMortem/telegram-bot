INITIAL_PRICE = 1
INITIAL_SUPPLY = 1000000000
F = 0.5


class User:
    def __init__(self):
        self.user_gold = 0
        self.user_silver = 1000


class Bancor:
    def __init__(self, token_supply):
        self.token_supply = token_supply

    def price(self):
        return (self.token_supply / INITIAL_SUPPLY) ** (1 / F - 1) * INITIAL_PRICE

    def calc_supply(self, tokens):
        return INITIAL_SUPPLY * ((1 + tokens / INITIAL_SUPPLY) ** F - 1)

    def buy_tokens(self, reserve_deposit):
        new_token_supply = self.calc_supply(reserve_deposit)
        self.token_supply += new_token_supply

    def sell_tokens(self, tokens_sold):
        new_token_supply = self.calc_supply(tokens_sold)
        self.token_supply -= new_token_supply


def buy_token(user: User, gold_amount, bancor: Bancor):
    silver_amount = gold_amount * bancor.price()
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
    user.user_silver += gold_amount / bancor.price()
    bancor.sell_tokens(gold_amount)


BANCOR = Bancor(INITIAL_SUPPLY)
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
            current_user
            print("USER1 -> USER2")
        else:
            current_user = USER
            print("USER2 -> USER1")

    else:
        print("Undefined command")

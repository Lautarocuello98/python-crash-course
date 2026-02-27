class User:
    def __init__(self, first_name, last_name, **user_info):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.profile = user_info 
        self.login_attempts = 0

    def describe_user(self):
        print(f"\nUser: {self.first_name} {self.last_name}")
        for key, value in self.profile.items():
            print(f"{key.title()}: {value}")

    def greet_user(self):
        print(f"Welcome back, {self.first_name}!")

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0


user1 = User(
    "lautaro",
    "cuello",
    age=28,
    email="lac1998123@gmail.com",
    country="Argentina",
    profession="Developer"
)

user2 = User(
    "ana",
    "martinez",
    age=25,
    email="ana@email.com"
)

users = [user1, user2]


for user in users:
    print()
    user.describe_user()
    user.greet_user()

    user.increment_login_attempts()
    print("Attempts now:", user.login_attempts)
    user.reset_login_attempts()
    print("\nUser log out, Attempts now:", user.login_attempts)

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

class Privileges:
    def __init__(self, privileges=None):
        if privileges is None:
            privileges = [
                "can add post",
                "can delete post",
                "can ban user",
            ]
        self.privileges = privileges

    def show_privileges(self):
        print("\nAdmin privileges:")
        if not self.privileges:
            print("- (no privileges assigned)")
            return

        for privilege in self.privileges:
            print(f"- {privilege}")


class Admin(User):
    def __init__(self, first_name, last_name, **user_info):
        super().__init__(first_name, last_name, **user_info)
        # Composition: Admin HAS a Privileges object
        self.privileges = Privileges()

admin1 = Admin(
    "lautaro",
    "cuello",
    age=28,
    email="lac1998123@gmail.com",
    country="Argentina",
    profession="Developer",
)
user1 = User(
    "ana",
    "martinez",
    age=25,
    email="ana@email.com"
)

admin1.describe_user()
admin1.greet_user()
admin1.privileges.show_privileges()

user1.describe_user()
user1.greet_user()
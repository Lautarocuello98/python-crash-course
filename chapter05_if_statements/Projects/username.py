usernames = ['admin', 'lautaro', 'jaden', 'maria', 'lucas']

new_users = ['Jaden', 'sofia', 'ADMIN', 'pedro', 'lucia']

usernames_lower = [user.lower() for user in usernames]

for user in new_users:
    if user.lower() in usernames_lower:
        print(f"Username {user} is already taken. Please choose a new one.")
    else:
        print(f"Username {user} is available.")
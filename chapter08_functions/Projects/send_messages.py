messages = [
    {'name': 'lili', 'message': 'Hello Lili! have a nice day'},
    {'name': 'dani', 'message': 'Hi Dani! see you this monday'},
    {'name': 'yaz', 'message': 'Nice to meet you Yaz'},
]

# ✅ copia real para no modificar la original
unsent_messages = messages[:]  
completed_messages = []


def show_messages(all_messages):
    print("\nThese are the messages to send:")
    for info in all_messages:
        print(f"{info['name']}: {info['message']}")


def send_messages(unsent_messages, completed_messages):
    print("\nSending messages:")
    while unsent_messages:
        current_message = unsent_messages.pop()
        print(f"Sending the message to {current_message['name']}")
        completed_messages.append(current_message)


def show_sent_messages(completed_messages):
    print("\nYou finished sending these messages:")
    for message in completed_messages:
        print(f"{message['name']}: {message['message']}")


show_messages(messages)
send_messages(unsent_messages, completed_messages)
show_sent_messages(completed_messages)

print("\nOriginal messages still intact:")
print(messages)
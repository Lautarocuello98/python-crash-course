def make_sandwich(*items):
    print("\nMaking a sandwich with:")
    for item in items:
        print(f"- {item}")

make_sandwich('ham', 'cheese')
make_sandwich('turkey', 'lettuce', 'tomato')
make_sandwich('peanut butter')
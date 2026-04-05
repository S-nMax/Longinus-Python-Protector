def display_message():
    part1 = "Hel"
    part2 = "lo"
    part3 = " Wor"
    part4 = "ld!"
    combined = part1 + part2 + part3 + part4
    return combined

def print_with_format(text):
    border = "-" * (len(text) + 4)
    formatted = f"| {text} |"
    print(border)
    print(formatted)
    print(border)

def main():
    message = display_message()
    if len(message) > 0:
        print_with_format(message)
    else:
        print("No message to display")

main()

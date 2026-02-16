def get_string(prompt: str) -> str:
    """
    Prompts the user for a string input and ensures it's not empty.
    Continuously retries if the user enters an empty string.
    """
    while True:
        s = input(prompt)

        if s and s.isalpha():
            return s.upper()

        print("輸入英文字母且不得留白")

def get_float(prompt: str) -> float:
    """
    Prompts the user for a number.
    Continuously retries if the input cannot be converted to a float.
    """

    while True:
        s = input(prompt)

        try:
            return float(s)
        except ValueError:
            print("輸入數字")
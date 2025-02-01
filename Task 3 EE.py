import random


def play_number_game():
    secret_number = random.randint(1, 100)
    guess_count = 0
    print("Welcome to the Ultimate Guessing Challenge!")
    print("I've chosen a number between 1 and 100. Can you find it?")

    while True:
        try:
            player_input = int(input("Enter your guess: "))
            guess_count += 1

            if player_input < 1 or player_input > 100:
                print("Your guess must be between 1 and 100.")
            elif player_input < secret_number:
                print("Too low! Try again.")
            elif player_input > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Awesome! You discovered the number in {guess_count} attempts.")
                break
        except ValueError:
            print("Oops! That’s not a valid number. Please try again.")


if __name__ == "__main__":
    play_number_game()

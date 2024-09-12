import random

num = random.randint(1, 100)
attempts = 0

while True:
    try:
        guess = int(input("Guess a number between 1 - 100: "))
        attempts += 1

        if guess > num:
            print("Your guess is too high! Try again.")
        elif guess < num:
            print("Your guess is too low! Try again.")
        else:
            print(f"Congratulations! You guessed the correct number in {attempts} attempts.")
            break

    except ValueError:
        print("Invalid input. Please enter a valid number between 1 and 100.")
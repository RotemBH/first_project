import random

VALID_INPUT = [str(i) for i in range(1, 10)] + ['exit']


def main():
    """
    a user need to guess a number between 1-9.
    he has many guess he wants.
    if he want to exit the game - insert exit
    :return:
    """
    need_to_guess = random.randint(1, 9)
    num_of_guess = 0
    while True:
        user_guess = input("please guess a number between 1-9: ")
        num_of_guess += 1
        if user_guess in VALID_INPUT:
            if user_guess == 'exit':
                print('bye bye!')
                return
            user_guess = int(user_guess)
            if user_guess < need_to_guess:
                print("you guess too low!")
            if user_guess > need_to_guess:
                print("you guess too high")

            if user_guess == need_to_guess:
                print(f"you guess right!, took you {num_of_guess} guess")
                need_to_guess = random.randint(1, 9)
                num_of_guess = 0

        else:
            print("you did not insert valid input. please insert number from 1-9, or exit.")


if __name__ == '__main__':
    main()

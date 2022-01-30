from random import randint
import prettytable
import json


def generate_numbers(num):
    """
    Generate a string of number random times.
    :param num: A number.
    :return: String of the number X times.
    """
    string = ""
    for _ in range(randint(1, 20)):
        string += str(num)
    return string


def check_input():
    """
    Check if the input is valid.
    :return: The valid input, as an int.
    """
    jump = input("How many steps do you want to take? ")
    if jump.isdigit():
        jump = int(jump)
        if 1 <= jump <= 600:
            return jump

        else:
            print("Please enter a number between 1 - 408")
            return check_input()

    else:
        print("Please enter a number...")
        return check_input()


def check_direction():
    """
    Check if the input is valid.
    :return: True if forward, False if backward.
    """
    direct = input("Do you want to move forward or backward? Type 'f' or 'b'. ").lower()
    if direct == 'f':
        return True
    elif direct == 'b':
        return False
    else:
        print("Please enter a valid input...")
        return check_direction()


def check_win(char):
    """
    Check if the player got to a letter.
    :param char: The current item.
    :return: True if there is no win. False if there is a win.
    """
    if char.isdigit():
        return True
    print("You've won!!!")
    return False


def print_high_score(score_list):
    """
    Print the Hall Of Fame table.
    :param score_list: List of high score.
    """
    tb = prettytable.PrettyTable()
    tb.field_names = ["Position", "Name", "Tries"]
    rank = 1
    for player in score_list:
        if player["Score"] > 0:
            tb.add_row([rank, player["Player"], player["Score"]])
        rank += 1
    print(tb)


def check_high_score(ls, score):
    """
    Check if you can enter the TOP 10.
    :param ls: High score data as json.
    :param score: The player score.
    :return: The updated data.
    """
    my_pos = -1
    for index in range(10):
        if ls["high_score"][index]["Score"] > score or ls["high_score"][index]["Score"] == 0:
            my_pos = index
            break

    if my_pos != -1:
        for index in range(9, my_pos, -1):
            ls["high_score"][index] = ls["high_score"][index - 1]

        ls["high_score"][my_pos] = {"Player": input("Enter your name: ").title(), "Score": score}
        print(f"You entered the HALL OF FAME. Placed: {my_pos + 1} ")
    return ls


# Create the file.
with open("Treasure_Island.txt", mode="w") as file:
    for number in range(10):
        file.write(generate_numbers(number))

    file.write("TREASURE")

    for number in range(9, -1, -1):
        file.write(generate_numbers(number))

print("Welcome to the Treasure Island Game!!")
game_is_on = True
turns = 0

# Open the file for the game.
with open("Treasure_Island.txt") as file:
    record = file.readline()
    file.seek(0)
    while game_is_on:
        if check_direction():
            turns += 1
            steps = check_input()
            file.seek(file.tell() + steps)
            if record[file.tell():file.tell() + 1] == "":
                print("You've passed the end of the file. You been moved back to the last char.")
                file.seek(len(record) - 1)
            print(record[file.tell():file.tell() + 1])
            game_is_on = check_win(record[file.tell():file.tell() + 1])
        else:
            steps = check_input()
            try:
                file.seek(file.tell() - steps)
            except ValueError:
                print("You cannot move backward. You at the beginning.")
            else:
                turns += 1
                print(record[file.tell():file.tell() + 1])
                game_is_on = check_win(record[file.tell():file.tell() + 1])

try:
    with open("High_Score.txt") as file:
        data = json.load(file)

except FileNotFoundError:
    with open("High_Score.txt", mode="w") as file:
        name = input("Enter your name: ").title()
        data = {"high_score": [{"Player": name, "Score": turns}]}
        for _ in range(2, 11):
            data["high_score"].append({"Player": "", "Score": 0})

else:
    data = check_high_score(data, turns)

finally:
    with open("High_Score.txt", mode="w") as file:
        json.dump(data, file, indent=4)

print_high_score(data["high_score"])

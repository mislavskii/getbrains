# preparing variables
import random
# default options. Key beaten by value(s)
beaten = {"scissors": ["rock"],
          "rock": ["paper"],
          "paper": ["scissors"]}

# initializing user session
name = input('Enter your name: ')
print(f'Hello, {name}')
score = 0
options = input().split(',')
if len(options) > 2:
    beaten = {}
    for option in options:
        shuffled = options[options.index(option)+1:] + options[
                            :options.index(option)]
        beaten[option] = shuffled[:len(options)//2]
print("Okay, let's start")

# checking if user has recorded score and loading it
with open('rating.txt', 'r') as scores:
    for line in scores:
        if name + ' ' in line:  # ' ' added to screen longer name variants
            score = int(line.split()[-1])
            break

# playing the game
while True:
    user = input()  # take user's move or command
    if user == '!exit':
        print('Bye!')
        break
    if user == '!rating':
        print(f'Your rating: {score}')
    elif user not in list(beaten.keys()):
        print('Invalid input')
    else:
        computer = random.choice(list(beaten.keys()))  # computer's move
        # determining the result by comparing user's and computer's moves
        if user == computer:
            print(f'There is a draw ({computer})')
            score += 50
        elif computer in beaten[user]:
            print(f'Sorry, but computer chose {computer}')
        else:
            print(f'Well done. Computer chose {computer} and failed')
            score += 100

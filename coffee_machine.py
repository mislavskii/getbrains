from random import randint


# creating coffee recipe template
class Recipe:
    def __init__(self, water, milk, beans, cost):
        self.ingredients = {'water': water,
                            'milk': milk,
                            'coffee beans': beans}
        self.cost = cost


# programming coffee machine
class CoffeeMachine:
    # configuring the coffee recipes
    espresso = Recipe(250, 0, 16, 4)
    latte = Recipe(350, 75, 20, 7)
    cappuccino = Recipe(200, 100, 12, 6)

    state = 'idle'

    # string chunks to be inserted in messages to user as appropriate
    fill_prompts = {'water': 'ml of water',
                    'milk': 'ml of milk',
                    'coffee beans': 'grams of coffee beans',
                    'cups': 'disposable coffee cups'}

    def __init__(self):
        # resources in machine on start
        self.resources = {'water': randint(0, 10) * 50,
                          'milk': randint(0, 10) * 25,
                          'coffee beans': randint(0, 10) * 4,
                          'cups': randint(0, 5),
                          'money': randint(0, 700)}

        self.action = None
        self.filling = None

    def interface(self):  # user interface
        if self.state == 'idle':
            return input('Write action (buy, fill, take, remaining, exit): ')
        if self.state == 'buy':
            return input('\nWhat do you want to buy? '
                         '1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ')
        if self.state == 'fill':
            return input(f'Write how many {self.fill_prompts[self.filling]} you are adding: ')

    def run(self):  # machine controller translating user commands into actions
        while True:
            self.action = self.interface()
            if self.action == 'buy':
                self.state = self.action
                self.buy(self.interface())
            if self.action == 'fill':
                print()
                self.state = self.action
                amounts = {}  # creating dictionary for each resource amount to be refilled
                for k in self.fill_prompts.keys():
                    self.filling = k
                    try:
                        amounts[k] = abs(int(self.interface()))
                    except:
                        amounts[k] = 0
                self.fill(amounts)  # invoking the fill method passing the dict as a parameter
            if self.action == 'take':
                self.take()
            if self.action == 'remaining':
                self.remaining()
            if self.action == 'exit':
                break

    def remaining(self):  # reporting current resources in the machine
        print()
        print('The coffee machine has:')
        for k, v in self.resources.items():
            print(f'{v} {self.fill_prompts[k]}' if k != 'money' else f'${v} of {k}')
        print()

    def enough(self, recipe):  # checking if there is enough resources to make a coffee
        for k, v in recipe.ingredients.items():
            if self.resources[k] < v:
                print(f'Sorry, not enough {k}!')
                return False
        if self.resources['cups'] < 1:
            print('Sorry, not enough disposable coffee cups!')
            return False
        return True

    def buy(self, order):  # serving a coffee
        if order not in ['1', '2', '3', 'back']:  # handling invalid input (surprise!)
                order = str(randint(1, 3))
        if order != 'back':
            orders = {'1': self.espresso,
                      '2': self.latte,
                      '3': self.cappuccino}
            recipe = orders[order]
            if self.enough(recipe):
                print('I have enough resources, making you a coffee!')
                for k, v in recipe.ingredients.items():
                    self.resources[k] -= v
                self.resources['cups'] -= 1
                self.resources['money'] += recipe.cost
        print()
        self.state = 'idle'

    def fill(self, amounts):  # refilling resources
        for k, v in amounts.items():
            self.resources[k] += v
        self.state = 'idle'
        print()

    def take(self):  # taking the money out
        print()
        print(f"I gave you ${self.resources['money']}")
        print()
        self.resources['money'] = 0


machine = CoffeeMachine()  # creating a coffee machine object
machine.run()  # running the machine

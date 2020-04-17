class CoffeeMachine:
    state = 'idle'

    # will be inserted in messages to user as appropriate
    fill_prompts = {'water': 'ml of water',
                    'milk': 'ml of milk',
                    'beans': 'grams of coffee beans',
                    'cups': 'disposable coffee cups'}

    def __init__(self):
        self.recipes = {'espresso': {'water': 250,
                                     'milk': 0,
                                     'beans': 16,
                                     'cost': 4},
                        'latte': {'water': 350,
                                  'milk': 75,
                                  'beans': 20,
                                  'cost': 7},
                        'cappuccino': {'water': 200,
                                       'milk': 100,
                                       'beans': 12,
                                       'cost': 6}
                        }

        # initial resources in machine on start
        self.resources = {'water': 400,
                          'milk': 540,
                          'beans': 120,
                          'cups': 9,
                          'money': 550}

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

    def run(self):  # machine controller
        while True:
            self.action = self.interface()
            if self.action == 'buy':
                self.state = self.action
                self.buy(self.interface())
            if self.action == 'fill':
                print()
                self.state = self.action
                amounts = {}
                for k in self.fill_prompts.keys():
                    self.filling = k
                    amounts[k] = int(self.interface())
                self.fill(amounts)
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
        for k in [k for k in self.recipes[recipe].keys() if k != 'cost']:
            if self.resources[k] < self.recipes[recipe][k]:
                print(f'Sorry, not enough {k}!')
                return False
        if self.resources['cups'] < 1:
            print('Sorry, not enough disposable coffee cups!')
            return False
        return True

    def buy(self, order):  # serving a coffee
        if order != 'back':
            orders = {'1': 'espresso',
                      '2': 'latte',
                      '3': 'cappuccino'}
            recipe = orders[order]
            if self.enough(recipe):
                print('I have enough resources, making you a coffee!')
                for k, v in self.recipes[recipe].items():
                    if k != 'cost':
                        self.resources[k] -= v
                self.resources['cups'] -= 1
                self.resources['money'] += self.recipes[recipe]['cost']
            print()
        self.state = 'idle'

    def fill(self, amounts):  # adding resources
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

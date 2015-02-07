from __future__ import print_function
import random


class Mastermind:
    
    class Config:
        def __init__(self, colors, positions, tries):
            self._colors = colors
            self._positions = positions
            self._tries = tries
            
        def colors(self):
            return self._colors
            
        def positions(self):
            return self._positions
            
        def tries(self):
            return self._tries
        
        def init_colors(self):
            u = list()
            for i in range(0, self.colors()):
                u.append(chr(ord('A')+i))
            return u

    class IO:
        def __init__(self):
            raise NotImplemented

        @staticmethod
        def wait_for_input(try_nr):
            try_combo = raw_input('Please type your try nr {}: '.format(try_nr))
            return try_combo
        
        @staticmethod
        def display_reward(reward, try_nr):
            print ('try nr {} results in: {}'.format(try_nr, reward))
        
        @staticmethod
        def win(tries):
            print('Congratulation! You win in {} tries'.format(tries))
            
        @staticmethod
        def lose(secret_code):
            print('You lose! Secret code was: {}'.format(secret_code))
        
        @staticmethod
        def caption(config):
            print ('"colors" are letters:', ''.join(config.init_colors()))
            print ('Secret code has {} positions'.format(config.positions()))
            print ('You have {} tries to discover it'.format(config.tries()))
            print ('Good luck!')
    
        @staticmethod
        def replay():
            input_ = raw_input('Do you want to play another game? (y/n) ')
            if input_.upper() == 'Y':
                return True
            else:
                return False
    
    class Reward(object):

        def __init__(self):
            self._list = []

        def __str__(self):
            return str(self._list)

        def append_black(self):
            self._list.append('B')
        
        def append_white(self):
            self._list.append('W')
        
        def blacks(self):
            val = 0
            for elem in self._list:
                if elem == 'B':
                    val += 1
            return val
        
        def whites(self):
            val = 0
            for elem in self._list:
                if elem == 'W':
                    val += 1
            return val        
        
        def finalize(self, config):
            while len(self._list) < config.positions():
                self._list.append('X')
            return self
        
        def is_a_win(self):
            return self.value() == 1.0
            
        def value(self):
            val = 0.0
            for item in self._list:
                if item == 'B':
                    val += 0.25
                elif item == 'W':
                    val += 0.031
            
            return val
        
    class State:
        def __init__(self, config):
            self._remaining_attempts = config.tries()
            self._victory = None
            self._config = config
            
        def current_attempt(self):
            return self._config.tries() - self._remaining_attempts + 1
        
        def next_attempt(self, victory):
            if victory:
                self._victory = True
            else:
                self._remaining_attempts -= 1
        
        def win(self):
            if self._victory is None:
                return False
            else:
                return self._victory
            
        def lose(self):
            return self._remaining_attempts <= 0

    class Combination(list):
        
        def compare(self, combo):
            reward = Mastermind.Reward()
            explored = list()
            for position in range(0, len(combo)):
                if combo[position] == self[position]:
                    reward.append_black()
                    explored.append(position)
            
            for position in range(0, len(combo)):
                if combo[position] != self[position]:
                    for i in range(0, len(self)):
                        if self[i] == combo[position] and i not in explored:
                            reward.append_white()
                            explored.append(i)
                            break
                            
            return reward
    
        def generate(self, config):
            color_set = config.init_colors()
            position_set = range(0, config.positions())
            
            colors = map(lambda x: random.choice(color_set), position_set)
            self.extend(colors)
                
            return self

    def __init__(self, colors=8, positions=4, tries=8):
        self._secret_code = None
        self._config = Mastermind.Config(colors, positions, tries)
        
    def generate_secret_code(self, display=False):
        self._secret_code = Mastermind.Combination().generate(self._config)
        if display:
            print(self._secret_code)
    
    def _interactive_game(self):
        game_state = Mastermind.State(self._config)
        
        while True:
            input_ = Mastermind.IO.wait_for_input(game_state.current_attempt())
            attempt = Mastermind.Combination(input_.upper())
            reward = self._secret_code.compare(attempt).finalize(self._config)
            Mastermind.IO.display_reward(reward, game_state.current_attempt())
            
            game_state.next_attempt(reward.is_a_win())
            if game_state.win():
                Mastermind.IO.win(game_state.current_attempt())
                break
            elif game_state.lose():
                Mastermind.IO.lose(self._secret_code)
                break
            else:
                continue
        
        if Mastermind.IO.replay():
            self.start()
        pass

    def start(self, caption=False, generate=True, interactive=True, input_generator=None, output_callback=None):
        
        if caption and interactive: 
            Mastermind.IO.caption(self._config)
        
        if generate: 
            self.generate_secret_code()
        
        if interactive:
            self._interactive_game()
        else:
            raise NotImplementedError
        

if __name__ == '__main__':
    game = Mastermind()
    game.generate_secret_code(display=False)
    game.start(caption=True, generate=False)


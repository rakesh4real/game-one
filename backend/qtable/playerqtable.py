import random
import numpy as np
from . initialdata import data
#from initialdata import data

class Agent:
    def __init__(self, gamma=0.9, lr=0.9):
        self.id2action = {
            0: 'ArrowUp',
            1: 'ArrowDown',
            2: 'ArrowRight',
            3: 'ArrowLeft',
        }
        self.action2id = dict([(v,k) for k, v in self.id2action.items()])

        self.n_actions = len(self.id2action.keys())
        self.n_states = data[4]['numRows'] * data[4]['numCols']
        self.qtable = np.zeros((self.n_states, self.n_actions)) # initial

        self.gamma = 0.9
        self.lr = 0.9
    
    def learn(self, s: int, a: int, r: float, s_new: int):
        """ updates q-table

        Q <- qtable[curstate][action]

        updateTerm = curR + gamma*maxQ_around_next_states + curQ  
        NewQ = { curQ } + lr { updateTerm }
        """
        update_term = (
            r +
            self.gamma * self.__max_Q_around_state(s_new) +
            self.qtable[s, a]
        )
        newQ = self.qtable[s, a] + self.lr*(update_term)

        # update q-table
        self.qtable[s, a] = newQ

        # LOG
        print('New Q Value: ', newQ)

    def __max_Q_around_state(self, s:int):
        Qs = self.qtable[s]
        return np.max(Qs)


    def make_move(self, s: int, epsilon:float=0):
        """
        Max { qtabel[curstate] } -> action
        """
        action_ids = np.array([i for i in range(self.n_actions)])

        #qs = self.qtable[s]
        qs = [44,202,77,11]
        maxq = np.max(qs)
        best_action = action_ids[ np.where(qs == maxq)[0] ][0]

        # epsilon[0,1] \propto randomness
        # epsilon = 0 --> always best moves
        randu = np.random.uniform(0, 1)
        if not (randu<epsilon): # extremely rarely makes exploitation as not using <=
            print('making random move')
            return random.randint(0,3)
        else:
            print('making best move')
            return best_action # not string.. id!

    @staticmethod
    def xy2state(x, y):
        """ map coods to states' ids 
            
        coods (x, y) correspond to:
           
             y: 0 + --- + --- + ----+
                  |     |     |     |  
             y: 1 + --- + --- + ----+ 
                  |     |     |     | 
             y: 2 + --- + --- + ----+ 
                  |     |     |     |
             y: ..+ --- + --- + ----+ 
                x: 0     1    2     3 
          
        
        """
        # stateid: in [0, 24]
        # coods: x in [0, 4] y in [0,4] 
        stateid = x*data[4]['numRows'] + y
        return stateid

    @staticmethod
    def getEpsilon(episode_num, total_episodes=50):
        """ 
        - epsilon \propto trainingPercent \propto explotation 
        - exploits more as reaches end of training
        """
        # todo: this is linear curve. Make it rectilinear
        training_per = episode_num / total_episodes
        return training_per

if __name__ == '__main__':
    a = Agent()
    for x in range(0, 5):
        for y in range(0,5):
            print(f'{x},{y}: {a.xy2state(x, y)}')
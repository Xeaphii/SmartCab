import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from QLearn import QLearn
import matplotlib.pyplot
import pylab

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.learning_rate = 0.5
        self.discounting_factor = 0.3
        self.default_val = 2
        self.max_trials = 100
        self.l_initial_state = None
        self.l_initial_action = None
        self.l_initial_reward = None
        self.x_hit = range(0,self.max_trials)
        self.y_hit = range(0,self.max_trials)
        self.y_steps = range(0,self.max_trials)
        self.counter = -1
        self.steps_counter = -1
        self.enforce_deadline = True
        self.update_delay=0
        self.display = False
        self.QLearner = QLearn(l_actions=Environment.valid_actions,l_learning_rate =self.learning_rate,l_discounting_factor =self.discounting_factor,l_default_val = self.default_val)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        print destination
        self.l_initial_state = None
        self.l_initial_action = None
        self.l_initial_reward = None		
        self.counter = self.counter + 1
        self.steps_counter = 0
        #print self.QLearner.states
		
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        self.steps_counter = self.steps_counter + 1
		
        print (inputs['light'],int(inputs['oncoming'] == 'right'),int(inputs['oncoming'] == 'left'))
        # TODO: Update state
        self.state=	 (inputs['light'],self.next_waypoint )
        # TODO: Select action according to your policy
        print 'self.state'
        print self.state
		
        action =self.QLearner.Get_action(self.state)
       
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.QLearner.update_Q(self.l_initial_state,self.l_initial_action,self.l_initial_reward,self.state)
        self.l_initial_state = self.state
        self.l_initial_action = action
        self.l_initial_reward = reward
        self.y_steps[self.counter] = self.steps_counter
        if (deadline == 0) & (reward < 10):
            self.y_hit[self.counter] = 0
        else:
            self.y_hit[self.counter] = 1		
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
	
    def plot_trials(self,x,y):
        matplotlib.pyplot.scatter(x,y)

        matplotlib.pyplot.show()

    def dynamic_gamma(self,gamma,max_value):
        return 	gamma/float(max_value)
		
def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=a.enforce_deadline)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=a.update_delay, display=a.display)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=a.max_trials)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    a.plot_trials(a.x_hit,a.y_hit)
    a.plot_trials(a.x_hit,a.y_steps)   

    for  k,v in a.QLearner.states.items():
        print(k, v)

if __name__ == '__main__':
    run()

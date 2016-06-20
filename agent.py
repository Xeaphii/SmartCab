import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from QLearn import QLearn

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.learning_rate = 0.5
        self.discounting_factor = 0.5
        self.default_val = 2
        self.QLearner = QLearn(l_actions=Environment.valid_actions,l_learning_rate =self.learning_rate,l_discounting_factor =self.discounting_factor,l_default_val = self.default_val)
        self.l_initial_state = None
        self.l_initial_action = None
        self.l_initial_reward = None
		
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        print destination

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

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
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=10)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()

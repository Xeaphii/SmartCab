import random

class QLearn:

   def __init__(self,l_actions, l_learning_rate = 0, l_discounting_factor = 0.5,l_default_val = 0):
      self.learning_rate = l_learning_rate
      self.discounting_factor = l_discounting_factor
      self.states = {}
      self.actions = l_actions
      self.default_val = l_default_val

   def get_Q_value(self,l_state,l_action):
      if (l_state,l_action) not in self.states:
         self.states[(l_state,l_action)] = self.default_val
      return self.states[(l_state,l_action)]

   def update_Q(self,l_state,l_action,l_reward,l_new_state):
      if l_state is not None:
            l_max = float("-inf")
            new_action = []
            for action in self.actions:
                  if l_max < self.get_Q_value(l_new_state,action):
                        l_max =  self.get_Q_value(l_new_state,action)
                        new_action = []				  
                        new_action.append( action)
                  elif l_max == self.get_Q_value(l_new_state,action):
                        new_action.append( action)
            action = 	new_action[random.randint(0, len(new_action))]	  
            self.states[(l_state,l_action)] = (1-self.learning_rate)*self.get_Q_value(l_state,l_action) +self.learning_rate*(l_reward+self.discounting_factor *l_max)  
	  
   def Get_action(self,l_state):
      if l_state is not None:
            l_max = float("-inf")
            new_action = []
            for action in self.actions:
                  if l_max < self.get_Q_value(l_state,action):
                        l_max =  self.get_Q_value(l_state,action)
                        new_action = []				  
                        new_action.append( action)
                  elif l_max == self.get_Q_value(l_state,action):
                        new_action.append( action)
            else:
			      new_action = self.actions
      action = 	new_action[random.randint(0, len(new_action))]	  
      return action
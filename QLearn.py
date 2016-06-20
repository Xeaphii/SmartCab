class QLearn:

   def __init__(self, l_learning_rate = 0, l_discounting_factor = 0.5,l_actions):
      self.learning_rate = l_learning_rate
      self.discounting_factor = l_discounting_factor
      self.states = {}
      self.actions = l_actions

   def get_Q_value(self,l_state,l_action):
      if (l_state,l_action) not in self.states:
         self.states[(l_state,l_action)] = 0
      return self.states[(l_state,l_action)]

   def update_Q(self,l_state,l_action,l_reward,l_new_state):
      l_max = float("-inf")
	  new_action = None
      for action in self.actions:
            if l_max > get_Q_value(self,l_new_state,action):
			      l_max =  get_Q_value(self,l_new_state,action)
				  new_action = action
      self.states[(l_state,l_action)] = (1-self.learning_rate)*self.states[(l_state,l_action)] +self.learning_rate*(self.discounting_factor *l_max)  
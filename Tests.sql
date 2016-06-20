from QLearn import QLearn
Q = QLearn(l_actions=['a','b'],l_learning_rate = 0.5,l_discounting_factor =0.5)
Q.update_Q(1,'a',1,2)
Q.get_Q_value(1,'a')

update_Q(self,l_state,l_action,l_reward,l_new_state):
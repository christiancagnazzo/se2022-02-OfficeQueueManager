from min import minWaitingTime
import unittest

class TestMinWaitingtime(unittest.TestCase):

    def test1(self):
        t_r = 5 #service time is 5 minutes
        n_r = 4 #4 people waiting for the same service,
        k_i = [2,1] # 2 service center offer 2 and 1 kind of service respectively
        s_i_r = [1,1] # all service offer this kind of service
        waitTime = minWaitingTime(t_r,n_r,k_i,s_i_r)
        self.assertEqual("15:50",waitTime)

if __name__ == '__main__':
    unittest.main()
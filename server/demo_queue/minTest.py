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
        
    def test2(self):
        t_r = 30 #service time is 30 minutes
        n_r = 40 #40 people waiting for the same service,
        k_i = [2,2,1] # 3 service center offer 2,2 and 1 kind of service respectively
        s_i_r = [1,1,1] # all service offer this kind of service
        waitTime = minWaitingTime(t_r,n_r,k_i,s_i_r)
        self.assertEqual("615:00",waitTime)
        
    def testCatchError(self):
        t_r = 30 #service time is 30 minutes
        n_r = 40 #40 people waiting for the same service,
        k_i = [2,2,1] # 3 service center offer 2,2 and 1 kind of service respectively
        s_i_r = [0,0,0] # no service offer this kind of service
        with self.assertRaises(ZeroDivisionError):
            waitTime = minWaitingTime(t_r,n_r,k_i,s_i_r)
            

if __name__ == '__main__':
    unittest.main()

import unittest
from src.simulation_game.agent import Agent

class TestAgents(unittest.TestCase):
    def test_infection_transmission(self):
        # Force a collision between I and S
        infected = Agent(100, 100, "I")
        susceptible = Agent(100, 100, "S")
        
        # Manually ensure random < 0.5 for test? 
        # Or check that state CHANGE is possible. 
        # Since logic is: if random < 0.5 then S->I.
        # Let's run it multiple times to ensure it can happen.
        transmitted = False
        for _ in range(20):
            susceptible.state = "S"
            infected.check_collision(susceptible)
            if susceptible.state == "I":
                transmitted = True
                break
        
        self.assertTrue(transmitted, "Infection should transmit eventually")

    def test_recovery(self):
        agent = Agent(0, 0, "I")
        agent.recovery_duration = 5
        agent.recovery_timer = 0
        
        for _ in range(5):
            agent.update()
            
        self.assertEqual(agent.state, "R")

if __name__ == '__main__':
    unittest.main()

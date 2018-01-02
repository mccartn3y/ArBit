"""Tests for retrieving ask and bid prices"""
import prices, unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_all_prices(self): 
        p = prices.AskAndBidGetter()
        print(p.get_all_eur_eth_prices())
        self.assertEqual(p.get_all_eur_eth_prices(), 0)

if __name__ == '__main__':
    unittest.main()
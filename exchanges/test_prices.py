"""Tests for retrieving ask and bid prices"""
import prices, unittest

class PricingTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_all_prices(self): 
        p = prices.AskAndBidGetter()
        print(p.get_all_eur_eth_prices())
        self.assertEqual(0, p.get_all_eur_eth_prices())

if __name__ == '__main__':
    unittest.main()
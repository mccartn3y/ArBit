"""Tests for GDAX Functions"""
import gdax_manager, requests, unittest

class GDAXTest(unittest.TestCase):

    def setUp(self, filename='GDAX_All.txt'):
        self.filename = filename
        self.order_manager = gdax_manager.GDAXOrderManager(self.filename)

    def test_get_all_open_eth_eur_orders(self):
        self.assertNotEqual(-1, self.order_manager.list_all_eth_eur_orders())

    # Note: Keep 1 cent in GDAX for testing purposes!
    def test_post_retrieve_then_delete_eth_eur_buy_order(self):
        # Post order
        limit_order_response = self.order_manager.post_eth_eur_limit_order(0.1, 0.01, 'buy')
        self.assertEqual(requests.codes.ok, limit_order_response.status_code)
        # Retrieve above order
        order_id = limit_order_response.json()['id']
        retrieve_order_response = self.order_manager.retrieve_eth_eur_limit_orders_by_id(order_id)
        self.assertEqual(requests.codes.ok, retrieve_order_response.status_code)
        self.assertEqual(0.1, float(retrieve_order_response.json()['size']))
        self.assertEqual(0.01, float(retrieve_order_response.json()['price']))
        # Delete order
        cancel_order_response = self.order_manager.cancel_eth_eur_limit_orders_by_id(order_id)
        self.assertEqual(requests.codes.ok, cancel_order_response.status_code)
        retrieve_cancelled_order_response = self.order_manager.retrieve_eth_eur_limit_orders_by_id(order_id)
        self.assertEqual(requests.codes.not_found, retrieve_cancelled_order_response.status_code)


if __name__ == '__main__':
    unittest.main()

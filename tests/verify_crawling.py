import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.crawler import CostcoCrawler
from src.models import Product

class TestCostcoCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = CostcoCrawler()
        self.crawler.session = MagicMock()

    def test_crawl_all_products_finds_categories(self):
        # Mock homepage response
        homepage_html = """
        <html>
            <nav>
                <a href="/c/category1">Category 1</a>
                <a href="/c/category2">Category 2</a>
                <a href="/other">Ignored</a>
            </nav>
        </html>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = homepage_html
        self.crawler.session.get.return_value = mock_response

        # Mock crawl_category to avoid actual recursion during this test
        with patch.object(self.crawler, 'crawl_category', return_value=[]) as mock_crawl_cat:
            self.crawler.crawl_all_products()
            
            # Check if session.get was called for homepage
            self.crawler.session.get.assert_any_call(self.crawler.BASE_URL, timeout=30)
            
            # Check if crawl_category was called for found categories
            # Note: The crawler deduplicates and iterates. Order might vary if set is used without sort, 
            # but we iterate a set so order is not guaranteed unless sorted.
            # In my code I used `for i, cat_url in enumerate(category_links):`
            # Let's check call count.
            self.assertEqual(mock_crawl_cat.call_count, 2)
            
            # Verify arguments (urls)
            calls = [args[0] for args, _ in mock_crawl_cat.call_args_list]
            self.assertIn("https://www.costco.com.tw/c/category1", calls)
            self.assertIn("https://www.costco.com.tw/c/category2", calls)

    def test_crawl_category_pagination(self):
        # Mock responses for pages
        # Page 0: has products
        # Page 1: has products
        # Page 2: no products (empty list)
        
        # We need to mock fetch_products_from_page
        with patch.object(self.crawler, 'fetch_products_from_page') as mock_fetch:
            # Side effect: return list of dummy products twice, then empty
            p1 = Product(id='1', name='P1', price='100', stock_status='In Stock', images=[], product_url='u1')
            p2 = Product(id='2', name='P2', price='200', stock_status='In Stock', images=[], product_url='u2')
            
            mock_fetch.side_effect = [[p1], [p2], []]
            
            products = self.crawler.crawl_category("http://test.com/c/cat")
            
            self.assertEqual(len(products), 2)
            self.assertEqual(mock_fetch.call_count, 3) # Page 0, 1, 2(empty)
            
            # 驗證 last_updated 欄位是否存在
            self.assertTrue(hasattr(products[0], 'last_updated'))
            self.assertIsNotNone(products[0].last_updated)
            
            # Verify URL handling
            calls = [args[0] for args, _ in mock_fetch.call_args_list]
            self.assertEqual(calls[0], "http://test.com/c/cat")
            self.assertEqual(calls[1], "http://test.com/c/cat?page=1")
            self.assertEqual(calls[2], "http://test.com/c/cat?page=2")

if __name__ == '__main__':
    unittest.main()

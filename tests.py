import unittest
import requests
from unittest.mock import patch, MagicMock
from for_tests import CatFactProcessor, APIError  

class TestCatFactProcessor(unittest.TestCase):

    @patch('requests.get')
    def test_get_fact_success(self, mock_get):
        # Настройка имитации успешного ответа API
        mock_response = MagicMock()
        mock_response.json.return_value = {"fact": "Cats are awesome!"}
        mock_get.return_value = mock_response
        
        processor = CatFactProcessor()
        fact = processor.get_fact()
        
        self.assertEqual(fact, "Cats are awesome!")
        self.assertIn(fact, processor.facts)

    @patch('requests.get')
    def test_get_fact_failure(self, mock_get):
        # Настройка имитации ошибки запроса
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        
        processor = CatFactProcessor()
        
        with self.assertRaises(APIError) as context:
            processor.get_fact()
        
        self.assertIn("Error request for API", str(context.exception))

    def test_get_fact_length_empty(self):
        # Тестируем длину факта, когда факты отсутствуют
        processor = CatFactProcessor()
        length = processor.get_fact_length()
        self.assertEqual(length, 0)

    @patch('requests.get')
    def test_get_fact_length_with_facts(self, mock_get):
        # Тестируем длину факта, когда факты присутствуют
        mock_response = MagicMock()
        mock_response.json.return_value = {"fact": "Cats are awesome!"}
        mock_get.return_value = mock_response
        
        processor = CatFactProcessor()
        processor.get_fact()  # Получаем факт
        length = processor.get_fact_length()
        self.assertEqual(length, len("Cats are awesome!"))

    def test_get_stats_empty(self):
        # Тестируем статистику, когда факты отсутствуют
        processor = CatFactProcessor()
        stats = processor.get_stats()
        self.assertEqual(stats, {"average": 0, "min": 0, "max": 0})

    @patch('requests.get')
    def test_get_stats_with_facts(self, mock_get):
        # Тестируем статистику, когда факты присутствуют
        mock_response = MagicMock()
        mock_response.json.return_value = {"fact": "Cats are awesome!"}
        mock_get.return_value = mock_response
        
        processor = CatFactProcessor(num_facts=3)
        processor.get_fact()  # Получаем первый факт
        processor.get_fact()  # Получаем второй факт
        
        stats = processor.get_stats()
        lengths = [len("Cats are awesome!")] * 2  # Два факта одинаковой длины
        self.assertEqual(stats["average"], sum(lengths) / len(lengths))
        self.assertEqual(stats["min"], min(lengths))
        self.assertEqual(stats["max"], max(lengths))

    @patch('requests.get')
    def test_get_stats_with_varying_fact_lengths(self, mock_get):
        # Тестируем статистику с фактами разной длины
        mock_responses = [
            {"fact": "Cats are awesome!"},
            {"fact": "I love cats!"},
            {"fact": "Cats are great companions."}
        ]
        
        mock_get.side_effect = [MagicMock(json=lambda: res) for res in mock_responses]
        
        processor = CatFactProcessor(num_facts=3)
        for _ in range(3):
            processor.get_fact()
        
        stats = processor.get_stats()
        lengths = [len(fact) for fact in ["Cats are awesome!", "I love cats!", "Cats are great companions."]]
        self.assertEqual(stats["average"], sum(lengths) / len(lengths))
        self.assertEqual(stats["min"], min(lengths))
        self.assertEqual(stats["max"], max(lengths))

if __name__ == '__main__':
    unittest.main()

import unittest
import sys
import os

def run_all_tests():
    print("=" * 60)
    print(" ЗАПУСК ТЕСТОВ ПРОЕКТА TAP")
    print("=" * 60)
    

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ:")
    print(f"   Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"    Ошибок: {len(result.failures)}")
    print(f"    Падений: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
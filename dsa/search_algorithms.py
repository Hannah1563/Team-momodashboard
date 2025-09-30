#!/usr/bin/env python3
"""
Data Structures & Algorithms Module for MoMo SMS Data Processing
Implements and compares different search algorithms for transaction data
"""

import time
import random
from typing import List, Dict, Any, Optional
from xml_parser import SMSDataParser
import os


class TransactionSearch:
    """Search algorithms for transaction data"""
    
    def __init__(self, transactions: List[Dict[str, Any]]):
        """
        Initialize with transaction data
        
        Args:
            transactions (List[Dict[str, Any]]): List of transaction dictionaries
        """
        self.transactions = transactions
        self.transaction_dict = self._build_dictionary()
        
    def _build_dictionary(self) -> Dict[int, Dict[str, Any]]:
        """
        Build dictionary for O(1) lookup by transaction ID
        
        Returns:
            Dict[int, Dict[str, Any]]: Dictionary mapping ID to transaction
        """
        return {transaction['id']: transaction for transaction in self.transactions}
    
    def linear_search_by_id(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Linear search to find transaction by ID
        Time Complexity: O(n)
        
        Args:
            transaction_id (int): ID of the transaction to find
            
        Returns:
            Optional[Dict[str, Any]]: Transaction data or None if not found
        """
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                return transaction
        return None
    
    def dictionary_lookup_by_id(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Dictionary lookup to find transaction by ID
        Time Complexity: O(1)
        
        Args:
            transaction_id (int): ID of the transaction to find
            
        Returns:
            Optional[Dict[str, Any]]: Transaction data or None if not found
        """
        return self.transaction_dict.get(transaction_id)
    
    def linear_search_by_amount_range(self, min_amount: float, max_amount: float) -> List[Dict[str, Any]]:
        """
        Linear search to find transactions within amount range
        Time Complexity: O(n)
        
        Args:
            min_amount (float): Minimum transaction amount
            max_amount (float): Maximum transaction amount
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        results = []
        for transaction in self.transactions:
            if min_amount <= transaction['amount'] <= max_amount:
                results.append(transaction)
        return results
    
    def linear_search_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:
        """
        Linear search to find transactions by type
        Time Complexity: O(n)
        
        Args:
            transaction_type (str): Type of transactions to find
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        results = []
        for transaction in self.transactions:
            if transaction['type'] == transaction_type:
                results.append(transaction)
        return results
    
    def binary_search_by_amount(self, target_amount: float) -> List[Dict[str, Any]]:
        """
        Binary search to find transactions with specific amount
        Requires sorted data by amount
        Time Complexity: O(log n)
        
        Args:
            target_amount (float): Amount to search for
            
        Returns:
            List[Dict[str, Any]]: List of transactions with target amount
        """
        # Sort transactions by amount for binary search
        sorted_transactions = sorted(self.transactions, key=lambda x: x['amount'])
        
        def binary_search_recursive(arr, target, left, right):
            if left > right:
                return []
            
            mid = (left + right) // 2
            
            if arr[mid]['amount'] == target:
                # Find all transactions with the same amount
                results = [arr[mid]]
                # Check left side
                i = mid - 1
                while i >= 0 and arr[i]['amount'] == target:
                    results.append(arr[i])
                    i -= 1
                # Check right side
                i = mid + 1
                while i < len(arr) and arr[i]['amount'] == target:
                    results.append(arr[i])
                    i += 1
                return results
            elif arr[mid]['amount'] < target:
                return binary_search_recursive(arr, target, mid + 1, right)
            else:
                return binary_search_recursive(arr, target, left, mid - 1)
        
        return binary_search_recursive(sorted_transactions, target_amount, 0, len(sorted_transactions) - 1)


class PerformanceAnalyzer:
    """Analyze performance of different search algorithms"""
    
    def __init__(self, search_engine: TransactionSearch):
        """
        Initialize with search engine
        
        Args:
            search_engine (TransactionSearch): Search engine instance
        """
        self.search_engine = search_engine
        self.results = {}
    
    def measure_search_performance(self, num_tests: int = 100) -> Dict[str, Any]:
        """
        Measure and compare performance of different search algorithms
        
        Args:
            num_tests (int): Number of test iterations
            
        Returns:
            Dict[str, Any]: Performance analysis results
        """
        transactions = self.search_engine.transactions
        
        if len(transactions) < 20:
            print("Warning: Less than 20 transactions available for meaningful comparison")
        
        # Generate random transaction IDs for testing
        available_ids = [t['id'] for t in transactions]
        test_ids = random.choices(available_ids, k=num_tests)
        
        # Test Linear Search
        linear_times = []
        for test_id in test_ids:
            start_time = time.time()
            self.search_engine.linear_search_by_id(test_id)
            end_time = time.time()
            linear_times.append(end_time - start_time)
        
        # Test Dictionary Lookup
        dict_times = []
        for test_id in test_ids:
            start_time = time.time()
            self.search_engine.dictionary_lookup_by_id(test_id)
            end_time = time.time()
            dict_times.append(end_time - start_time)
        
        # Calculate statistics
        linear_avg = sum(linear_times) / len(linear_times)
        dict_avg = sum(dict_times) / len(dict_times)
        
        # Test Binary Search (for amount-based searches)
        binary_times = []
        test_amounts = [random.choice(transactions)['amount'] for _ in range(num_tests)]
        for amount in test_amounts:
            start_time = time.time()
            self.search_engine.binary_search_by_amount(amount)
            end_time = time.time()
            binary_times.append(end_time - start_time)
        
        binary_avg = sum(binary_times) / len(binary_times)
        
        results = {
            'total_transactions': len(transactions),
            'test_iterations': num_tests,
            'linear_search': {
                'average_time': linear_avg,
                'total_time': sum(linear_times),
                'min_time': min(linear_times),
                'max_time': max(linear_times)
            },
            'dictionary_lookup': {
                'average_time': dict_avg,
                'total_time': sum(dict_times),
                'min_time': min(dict_times),
                'max_time': max(dict_times)
            },
            'binary_search': {
                'average_time': binary_avg,
                'total_time': sum(binary_times),
                'min_time': min(binary_times),
                'max_time': max(binary_times)
            },
            'performance_comparison': {
                'linear_vs_dict_speedup': linear_avg / dict_avg if dict_avg > 0 else float('inf'),
                'linear_vs_binary_speedup': linear_avg / binary_avg if binary_avg > 0 else float('inf'),
                'dict_vs_binary_speedup': dict_avg / binary_avg if binary_avg > 0 else float('inf')
            }
        }
        
        self.results = results
        return results
    
    def print_performance_report(self):
        """Print detailed performance analysis report"""
        if not self.results:
            print("No performance data available. Run measure_search_performance() first.")
            return
        
        print("=" * 60)
        print("SEARCH ALGORITHM PERFORMANCE ANALYSIS")
        print("=" * 60)
        print(f"Total Transactions: {self.results['total_transactions']}")
        print(f"Test Iterations: {self.results['test_iterations']}")
        print()
        
        # Linear Search Results
        linear = self.results['linear_search']
        print("LINEAR SEARCH (O(n)):")
        print(f"  Average Time: {linear['average_time']:.8f} seconds")
        print(f"  Total Time: {linear['total_time']:.6f} seconds")
        print(f"  Min Time: {linear['min_time']:.8f} seconds")
        print(f"  Max Time: {linear['max_time']:.8f} seconds")
        print()
        
        # Dictionary Lookup Results
        dict_lookup = self.results['dictionary_lookup']
        print("DICTIONARY LOOKUP (O(1)):")
        print(f"  Average Time: {dict_lookup['average_time']:.8f} seconds")
        print(f"  Total Time: {dict_lookup['total_time']:.6f} seconds")
        print(f"  Min Time: {dict_lookup['min_time']:.8f} seconds")
        print(f"  Max Time: {dict_lookup['max_time']:.8f} seconds")
        print()
        
        # Binary Search Results
        binary = self.results['binary_search']
        print("BINARY SEARCH (O(log n)):")
        print(f"  Average Time: {binary['average_time']:.8f} seconds")
        print(f"  Total Time: {binary['total_time']:.6f} seconds")
        print(f"  Min Time: {binary['min_time']:.8f} seconds")
        print(f"  Max Time: {binary['max_time']:.8f} seconds")
        print()
        
        # Performance Comparison
        comparison = self.results['performance_comparison']
        print("PERFORMANCE COMPARISON:")
        print(f"  Dictionary is {comparison['linear_vs_dict_speedup']:.2f}x faster than Linear Search")
        print(f"  Binary Search is {comparison['linear_vs_binary_speedup']:.2f}x faster than Linear Search")
        print(f"  Dictionary is {comparison['dict_vs_binary_speedup']:.2f}x faster than Binary Search")
        print()
        
        print("ANALYSIS:")
        print("- Dictionary lookup (O(1)) is significantly faster for ID-based searches")
        print("- Binary search (O(log n)) is efficient for sorted data searches")
        print("- Linear search (O(n)) is simple but slower for large datasets")
        print("- For unsorted data, dictionary lookup provides the best performance")
        print("- Binary search requires data to be sorted, adding preprocessing overhead")


def main():
    """Main function to demonstrate search algorithms"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    xml_file_path = os.path.join(project_root, 'data', 'raw', 'modified_sms_v2.xml')
    
    # Parse XML data
    parser = SMSDataParser(xml_file_path)
    transactions = parser.parse_xml()
    
    if not transactions:
        print("No transactions found. Please check the XML file.")
        return
    
    print(f"Loaded {len(transactions)} transactions for analysis")
    print()
    
    # Initialize search engine
    search_engine = TransactionSearch(transactions)
    
    # Demonstrate different search methods
    print("SEARCH DEMONSTRATIONS:")
    print("-" * 30)
    
    # Search by ID
    transaction_5 = search_engine.linear_search_by_id(5)
    if transaction_5:
        print(f"Linear Search - Transaction 5: {transaction_5['type']} - {transaction_5['amount']} {transaction_5['currency']}")
    
    transaction_5_dict = search_engine.dictionary_lookup_by_id(5)
    if transaction_5_dict:
        print(f"Dictionary Lookup - Transaction 5: {transaction_5_dict['type']} - {transaction_5_dict['amount']} {transaction_5_dict['currency']}")
    
    # Search by amount range
    amount_range_results = search_engine.linear_search_by_amount_range(10000, 20000)
    print(f"Transactions between 10,000-20,000 RWF: {len(amount_range_results)} found")
    
    # Search by type
    transfer_results = search_engine.linear_search_by_type('Transfer')
    print(f"Transfer transactions: {len(transfer_results)} found")
    
    # Binary search by amount
    binary_results = search_engine.binary_search_by_amount(5000.0)
    print(f"Binary search for 5000 RWF: {len(binary_results)} found")
    
    print()
    
    # Performance Analysis
    print("PERFORMANCE ANALYSIS:")
    print("-" * 20)
    analyzer = PerformanceAnalyzer(search_engine)
    analyzer.measure_search_performance(num_tests=100)
    analyzer.print_performance_report()


if __name__ == "__main__":
    main()

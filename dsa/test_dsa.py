#!/usr/bin/env python3

import os
import sys
import time
from xml_parser import SMSDataParser
from search_algorithms import TransactionSearch, PerformanceAnalyzer


def test_xml_parsing():
    print("=" * 60)
    print("XML PARSING TEST")
    print("=" * 60)
    
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    xml_file_path = os.path.join(project_root, 'data', 'raw', 'modified_sms_v2.xml')
    
    print(f"Testing XML file: {xml_file_path}")
    print()
    
    # Test XML parsing
    parser = SMSDataParser(xml_file_path)
    transactions = parser.parse_xml()
    
    if transactions:
        print(f"Successfully parsed {len(transactions)} transactions")
        print()
        
        # Display sample transactions
        print("Sample Transactions:")
        print("-" * 20)
        for i, transaction in enumerate(transactions[:3]):
            print(f"{i+1}. ID: {transaction['id']}, Type: {transaction['type']}, "
                  f"Amount: {transaction['amount']} {transaction['currency']}")
        print()
        
        return transactions
    else:
        print("Failed to parse XML file")
        return []


def test_search_algorithms(transactions):
    if not transactions:
        print("No transactions available for search testing")
        return
    
    print()
    print("=" * 60)
    print("SEARCH ALGORITHM PERFORMANCE TEST")
    print("=" * 60)
    
    # Initialize search engine
    search_engine = TransactionSearch(transactions)
    
    print(f"Testing with {len(transactions)} transactions")
    print()
    
    # Test different search methods
    print("Search Method Demonstrations:")
    print("-" * 35)
    
    # Test ID-based searches
    test_id = 10
    print(f"Searching for transaction ID {test_id}:")
    
    # Linear search
    start_time = time.time()
    linear_result = search_engine.linear_search_by_id(test_id)
    linear_time = time.time() - start_time
    
    # Dictionary lookup
    start_time = time.time()
    dict_result = search_engine.dictionary_lookup_by_id(test_id)
    dict_time = time.time() - start_time
    
    print(f"  Linear Search: {linear_time:.8f}s - {'Found' if linear_result else 'Not found'}")
    print(f"  Dictionary Lookup: {dict_time:.8f}s - {'Found' if dict_result else 'Not found'}")
    print()
    
    # Test amount range search
    print("Searching for transactions between 10,000-20,000 RWF:")
    start_time = time.time()
    range_results = search_engine.linear_search_by_amount_range(10000, 20000)
    range_time = time.time() - start_time
    print(f"  Found {len(range_results)} transactions in {range_time:.8f}s")
    print()
    
    # Test type search
    print("Searching for Transfer transactions:")
    start_time = time.time()
    type_results = search_engine.linear_search_by_type('Transfer')
    type_time = time.time() - start_time
    print(f"  Found {len(type_results)} transactions in {type_time:.8f}s")
    print()
    
    # Test binary search
    print("Binary search for transactions with 5000 RWF:")
    start_time = time.time()
    binary_results = search_engine.binary_search_by_amount(5000.0)
    binary_time = time.time() - start_time
    print(f"  Found {len(binary_results)} transactions in {binary_time:.8f}s")
    print()
    
    # Performance analysis
    print("Performance Analysis:")
    print("-" * 20)
    analyzer = PerformanceAnalyzer(search_engine)
    analyzer.measure_search_performance(num_tests=100)
    analyzer.print_performance_report()


def test_data_structures():
    print()
    print("=" * 60)
    print("DATA STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Get transactions
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    xml_file_path = os.path.join(project_root, 'data', 'raw', 'modified_sms_v2.xml')
    
    parser = SMSDataParser(xml_file_path)
    transactions = parser.parse_xml()
    
    if not transactions:
        print("No transactions available for data structure testing")
        return
    
    print(f"Analyzing {len(transactions)} transactions")
    print()
    
    # List vs Dictionary comparison
    print("Data Structure Comparison:")
    print("-" * 30)
    
    # List (linear search)
    print("List Implementation:")
    start_time = time.time()
    for i in range(100):
        for transaction in transactions:
            if transaction['id'] == 5:
                break
    list_time = time.time() - start_time
    print(f"  Linear search (100 iterations): {list_time:.6f}s")
    
    # Dictionary (hash lookup)
    transaction_dict = {t['id']: t for t in transactions}
    print("Dictionary Implementation:")
    start_time = time.time()
    for i in range(100):
        transaction_dict.get(5)
    dict_time = time.time() - start_time
    print(f"  Hash lookup (100 iterations): {dict_time:.6f}s")
    
    speedup = list_time / dict_time if dict_time > 0 else float('inf')
    print(f"  Dictionary is {speedup:.2f}x faster than List")
    print()
    
    # Memory usage analysis
    import sys
    
    list_size = sys.getsizeof(transactions)
    dict_size = sys.getsizeof(transaction_dict)
    
    print("Memory Usage:")
    print(f"  List size: {list_size} bytes")
    print(f"  Dictionary size: {dict_size} bytes")
    print(f"  Memory overhead: {dict_size - list_size} bytes")
    print()
    
    # Algorithm complexity analysis
    print("Algorithm Complexity Analysis:")
    print("-" * 35)
    print("Linear Search:")
    print("  - Time Complexity: O(n)")
    print("  - Space Complexity: O(1)")
    print("  - Best Case: O(1) - element at first position")
    print("  - Worst Case: O(n) - element at last position")
    print("  - Average Case: O(n/2)")
    print()
    
    print("Dictionary Lookup:")
    print("  - Time Complexity: O(1) average case")
    print("  - Space Complexity: O(n)")
    print("  - Best Case: O(1)")
    print("  - Worst Case: O(n) - hash collision")
    print("  - Average Case: O(1)")
    print()
    
    print("Binary Search:")
    print("  - Time Complexity: O(log n)")
    print("  - Space Complexity: O(1)")
    print("  - Requires: Sorted data")
    print("  - Best Case: O(1)")
    print("  - Worst Case: O(log n)")
    print("  - Average Case: O(log n)")


def demonstrate_alternative_structures():
    print()
    print("=" * 60)
    print("ALTERNATIVE DATA STRUCTURES")
    print("=" * 60)
    
    print("For improved performance, consider these alternatives:")
    print()
    
    print("1. B-Tree:")
    print("   - Balanced tree structure")
    print("   - Efficient for range queries")
    print("   - Good for large datasets")
    print("   - Time Complexity: O(log n)")
    print()
    
    print("2. Red-Black Tree:")
    print("   - Self-balancing binary search tree")
    print("   - Guarantees O(log n) operations")
    print("   - Good for dynamic data")
    print("   - Time Complexity: O(log n)")
    print()
    
    print("3. Skip List:")
    print("   - Probabilistic data structure")
    print("   - Simple implementation")
    print("   - Good average performance")
    print("   - Time Complexity: O(log n)")
    print()
    
    print("4. Trie (Prefix Tree):")
    print("   - Efficient for prefix searches")
    print("   - Good for phone number lookups")
    print("   - Space-time tradeoff")
    print("   - Time Complexity: O(m) where m is key length")
    print()
    
    print("5. Hash Table with Chaining:")
    print("   - Handles collisions gracefully")
    print("   - Good average performance")
    print("   - Simple implementation")
    print("   - Time Complexity: O(1) average, O(n) worst case")


def main():
    print("MoMo SMS Data Structures & Algorithms Test Suite")
    print("=" * 60)
    print()
    
    # Test XML parsing
    transactions = test_xml_parsing()
    
    # Test search algorithms
    test_search_algorithms(transactions)
    
    # Test data structures
    test_data_structures()
    
    # Demonstrate alternatives
    demonstrate_alternative_structures()
    
    print()
    print("=" * 60)
    print("DSA TESTING COMPLETE")
    print("=" * 60)
    print("All DSA tests completed successfully!")

if __name__ == "__main__":
    main()

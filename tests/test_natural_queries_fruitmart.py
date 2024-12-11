import pytest
from querycraft.utils.db_connector import DatabaseConnector

@pytest.fixture
def db():
    return DatabaseConnector(schema_name="fruitmart")

def test_natural_language_queries(db):
    """Test natural language queries return correct database results"""
    
    test_cases = [
        {
            "question": "Which fruits in basket A contain the letter 'a'?(case insensitive)",
            "expected_results": ['Apple', 'Apple', 'Orange', 'Banana']
        },
        {
            "question": "How many fruits are in basket B?",
            "expected_results": ["8"]
        },
        {
            "question": "How many rows are there where both basket_a and basket_b have a NULL ID?",
            "expected_results": ["9"]
        },
        {
            "question": "How many distinct IDs in basket_a are greater than any of the IDs in basket_b?",
            "expected_results": ["3"]
        },
        {
            "question": "How many rows in basket_b have matching IDs with basket_a, and for those rows, how many also have a matching fruit in basket_a?",
            "expected_results": ["7"]
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting question: {case['question']}")
        
        try:
            result = db.execute_natural_query(case["question"])
            
            if "expected_result" in case:
                actual_results = result["result"].strip().split('\n') if result["result"] != "No results found" else []
                assert sorted(actual_results) == sorted(case["expected_result"]), (
                    f"Results don't match for question: {case['question']}\n"
                    f"Expected: {case['expected_result']}\n"
                    f"Got: {actual_results}"
                )
                print(f"✓ Results matched: {result['result']}")
            else:
                print(f"Warning: No expected_result defined for question: {case['question']}")
            
        except KeyError as e:
            print(f"\nMissing key in test case or result:")
            print(f"Question: {case['question']}")
            print(f"Error: {str(e)}")
            pytest.fail(f"Test case configuration error: {str(e)}")
            
        except Exception as e:
            print(f"\nDetailed error information:")
            print(f"Question: {case['question']}")
            print(f"Error: {str(e)}")
            pytest.fail(f"Error for question '{case['question']}': {str(e)}")

def test_edge_cases(db):
    """Test edge cases and error handling"""
    
    test_cases = [
        {
            "question": "Find fruits that don't exist",
            "expected_result": "No results found"
        },
        {
            "question": "Show fruits in basket A where price > 10",
            "expected_result": "No results found"
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting edge case: {case['question']}")
        
        try:
            result = db.execute_natural_query(case["question"])
           
            if "expected_result" in case:
                assert result["result"] == case["expected_result"]
                print(f"✓ Successfully handled: {case['question']}")
            
            if "expected_error" in case:
                pytest.fail(f"Expected an error but got success: {result}")
            
        except Exception as e:
            if "expected_error" in case:
                error_msg = str(e).lower()
                found_expected = any(exp.lower() in error_msg for exp in case["expected_error"])
                assert found_expected, (
                    f"Wrong error message for question: {case['question']}\n"
                    f"Expected to find one of: {case['expected_error']}\n"
                    f"Got: {str(e)}"
                )
                print(f"✓ Successfully caught expected error about schema/query limitation")
            else:
                pytest.fail(f"Unexpected error for '{case['question']}': {str(e)}")

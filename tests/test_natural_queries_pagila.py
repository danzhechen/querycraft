import pytest
from src.utils.db_connector import DatabaseConnector

@pytest.fixture
def db():
    return DatabaseConnector(schema_name="pagila")

def test_natural_language_queries(db):
    """Test natural language queries return correct database results"""
    
    test_cases = [
        {
            "question": "Find the actor_id of every actor whose first name starts with 'j'. Order the results from low to high.",
            "validation": {
                "count": 23,
                "first": "4",
                "last": "199",
                "is_ordered": True
            }
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting question: {case['question']}")
        
        try:
            result = db.execute_natural_query(case["question"])
            actual_results = result["result"].strip().split('\n') if result["result"] != "No results found" else []
            
            assert len(actual_results) == case["validation"]["count"], (
                f"Result count doesn't match. Expected {case['validation']['count']}, got {len(actual_results)}"
            )
            
            assert actual_results[0] == case["validation"]["first"], (
                f"First result doesn't match. Expected {case['validation']['first']}, got {actual_results[0]}"
            )
            
            assert actual_results[-1] == case["validation"]["last"], (
                f"Last result doesn't match. Expected {case['validation']['last']}, got {actual_results[-1]}"
            )
            
            if case["validation"]["is_ordered"]:
                assert actual_results == sorted(actual_results), "Results are not properly ordered"
            
            print(f"✓ Results matched the validation criteria")
            
        except Exception as e:
            print(f"\nDetailed error information:")
            print(f"Question: {case['question']}")
            print(f"Error: {str(e)}")
            pytest.fail(f"Error for question '{case['question']}': {str(e)}")
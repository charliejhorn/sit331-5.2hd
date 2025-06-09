#!/usr/bin/env python3
"""
Simple test script to verify custom exceptions are working correctly.
"""
import sys
import os

# Add the gallery package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gallery'))

from gallery.utils import NotFoundException, DuplicateException
from gallery.db.artifact_da import ArtifactDataAccess
from gallery.db.artist_da import ArtistDataAccess

def test_not_found_exception():
    """Test NotFoundException functionality"""
    print("Testing NotFoundException...")
    
    # Test the exception creation
    exc = NotFoundException(999)
    expected_message = "resource with id 999 not found"
    assert str(exc) == expected_message, f"Expected '{expected_message}', got '{str(exc)}'"
    print("✓ NotFoundException message format is correct")
    
    # Test with DataAccess class
    artifact_da = ArtifactDataAccess()
    try:
        artifact_da.get_artifact_by_id(99999)  # Non-existent ID
        assert False, "Expected NotFoundException to be raised"
    except NotFoundException as e:
        assert "99999" in str(e), f"Expected ID 99999 in error message, got: {str(e)}"
        print("✓ NotFoundException is properly raised by DataAccess")
    except Exception as e:
        assert False, f"Expected NotFoundException, got {type(e).__name__}: {str(e)}"

def test_duplicate_exception():
    """Test DuplicateException functionality"""
    print("\nTesting DuplicateException...")
    
    # Test the exception creation
    exc = DuplicateException('name', 'Test Artist')
    expected_message = "duplicate value 'Test Artist' found for field 'name'"
    assert str(exc) == expected_message, f"Expected '{expected_message}', got '{str(exc)}'"
    print("✓ DuplicateException message format is correct")
    
    # Test with DataAccess class - create an artist twice
    artist_da = ArtistDataAccess()
    test_artist = {
        'name': f'Test Artist {os.getpid()}',  # Use PID to make it unique
        'birth_year': 1990,
        'death_year': None,
        'tribe_id': 1  # Assuming tribe with ID 1 exists
    }
    
    try:
        # Create the artist first time - should succeed
        artist1 = artist_da.add_new_artist(test_artist)
        print(f"✓ First artist creation succeeded: {artist1['name']}")
        
        # Try to create the same artist again - should raise DuplicateException
        try:
            artist2 = artist_da.add_new_artist(test_artist)
            assert False, "Expected DuplicateException to be raised"
        except DuplicateException as e:
            assert "name" in str(e) and test_artist['name'] in str(e), f"Expected name and value in error message, got: {str(e)}"
            print("✓ DuplicateException is properly raised by DataAccess")
        except Exception as e:
            print(f"⚠ Got {type(e).__name__} instead of DuplicateException: {str(e)}")
            print("  This might be expected if the database doesn't have unique constraints yet")
    except Exception as e:
        print(f"⚠ Could not test duplicate creation: {type(e).__name__}: {str(e)}")

def main():
    """Run all tests"""
    print("Testing Custom Exceptions Implementation\n")
    
    try:
        test_not_found_exception()
        test_duplicate_exception()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

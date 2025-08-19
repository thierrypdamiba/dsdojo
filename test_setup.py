#!/usr/bin/env python3
"""
Test script to verify the Qdrant workshop setup
Run this after setup to ensure everything is working
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    required_packages = [
        ("qdrant_client", "Qdrant Client"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("tqdm", "TQDM"),
        ("matplotlib", "Matplotlib"),
        ("sklearn", "Scikit-learn")
    ]
    
    all_good = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            all_good = False
    
    return all_good

def test_utils():
    """Test if utils.py can be imported and used"""
    print("\n🔍 Testing utils.py...")
    
    try:
        from utils import create_sample_dataset, print_system_info
        print("   ✅ utils.py imported successfully")
        
        # Test sample dataset creation
        df = create_sample_dataset(size=5, seed=42)
        print(f"   ✅ Sample dataset created: {len(df)} rows")
        
        # Test system info
        print_system_info()
        
        return True
    except Exception as e:
        print(f"   ❌ utils.py test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔍 Testing environment configuration...")
    
    # Check if .env exists
    if os.path.exists('.env'):
        print("   ✅ .env file found")
        
        # Check if it contains real values
        with open('.env', 'r') as f:
            content = f.read()
            if 'your-cluster.qdrant.io' in content or 'your-api-key' in content:
                print("   ⚠️  .env contains placeholder values - please update with real credentials")
                return False
            else:
                print("   ✅ .env appears to be configured")
                return True
    else:
        print("   ❌ .env file not found - please run setup script first")
        return False

def test_jupyter():
    """Test if JupyterLab is available"""
    print("\n🔍 Testing JupyterLab...")
    
    try:
        import jupyterlab
        print("   ✅ JupyterLab available")
        return True
    except ImportError:
        print("   ❌ JupyterLab not available - run: pip install jupyterlab")
        return False

def main():
    """Run all tests"""
    print("🧪 Qdrant Workshop Setup Test")
    print("=" * 40)
    
    tests = [
        ("Package Imports", test_imports),
        ("Utils Module", test_utils),
        ("Environment Config", test_environment),
        ("JupyterLab", test_jupyter)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your setup is ready.")
        print("Next steps:")
        print("1. Launch JupyterLab: jupyter lab")
        print("2. Open 01_fundamentals.ipynb")
        print("3. Follow the workshop!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Common solutions:")
        print("- Run setup script: ./setup.sh (Linux/Mac) or setup.bat (Windows)")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Configure .env file with your Qdrant Cloud credentials")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

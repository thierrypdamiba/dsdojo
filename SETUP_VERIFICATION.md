# ✅ Setup Verification Guide

This document explains how to verify that your Qdrant workshop setup is working correctly.

## 🧪 Run the Test Script

The easiest way to verify your setup is to run the automated test:

```bash
python3 test_setup.py
```

### Expected Output (Success)
```
🧪 Qdrant Workshop Setup Test
========================================
🔍 Testing package imports...
   ✅ Qdrant Client
   ✅ NumPy
   ✅ Pandas
   ✅ TQDM
   ✅ Matplotlib
   ✅ Scikit-learn

🔍 Testing utils.py...
   ✅ utils.py imported successfully
   ✅ Sample dataset created: 5 rows

🔍 Testing environment configuration...
   ✅ .env file found
   ⚠️  .env contains placeholder values - please update with real credentials

🔍 Testing JupyterLab...
   ✅ JupyterLab available

========================================
📊 Test Results Summary
========================================
Package Imports: ✅ PASS
Utils Module: ✅ PASS
Environment Config: ⚠️  WARNING (expected)
JupyterLab: ✅ PASS

Overall: 3/4 tests passed

⚠️  .env contains placeholder values - this is expected until you add real credentials
```

## 🔍 Manual Verification Steps

### 1. Check Package Imports
```python
# Test in Python console or notebook
import qdrant_client
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
print("✅ All packages imported successfully!")
```

### 2. Test Utils Module
```python
from utils import create_sample_dataset, print_system_info

# Create sample data
df = create_sample_dataset(size=10, seed=42)
print(f"✅ Sample dataset created: {len(df)} rows")

# Print system info
print_system_info()
```

### 3. Verify JupyterLab
```bash
jupyter lab --version
# Should show version 4.0+
```

### 4. Check File Structure
```bash
ls -la
# Should show:
# - 01_fundamentals.ipynb
# - utils.py
# - requirements.txt
# - README.md
# - .env (created from env.example)
```

## 🚨 Common Issues and Solutions

### Issue: Import Errors
**Symptoms**: `ModuleNotFoundError` or `ImportError`
**Solution**: Install missing packages
```bash
pip3 install -r requirements.txt
# or for minimal install:
pip3 install -r requirements-minimal.txt
```

### Issue: JupyterLab Won't Start
**Symptoms**: `jupyter: command not found` or startup errors
**Solution**: Install/upgrade JupyterLab
```bash
pip3 install --upgrade jupyterlab
```

### Issue: .env File Missing
**Symptoms**: "Environment configuration failed" in test
**Solution**: Create .env file
```bash
cp env.example .env
# Then edit .env with your real credentials
```

### Issue: SSL Warnings
**Symptoms**: urllib3 warnings about OpenSSL
**Solution**: This is just a warning and won't affect functionality
```bash
# Optional: upgrade urllib3
pip3 install --upgrade urllib3
```

## 🎯 What Success Looks Like

When your setup is working correctly, you should be able to:

1. ✅ **Import all required packages** without errors
2. ✅ **Use the utils module** to create sample datasets
3. ✅ **Launch JupyterLab** and open notebooks
4. ✅ **Run the first notebook** (01_fundamentals.ipynb) successfully
5. ⚠️ **Configure .env** with real Qdrant Cloud credentials (required for actual workshop)

## 🚀 Next Steps After Verification

1. **Get Qdrant Cloud credentials** at [cloud.qdrant.io](https://cloud.qdrant.io)
2. **Edit .env file** with your real credentials
3. **Launch JupyterLab**: `jupyter lab`
4. **Open 01_fundamentals.ipynb** and start the workshop!

## 🔧 Troubleshooting Commands

```bash
# Check Python version
python3 --version

# Check pip version
pip3 --version

# List installed packages
pip3 list | grep -E "(qdrant|pandas|numpy|matplotlib)"

# Test specific import
python3 -c "import qdrant_client; print('Qdrant client works!')"

# Check JupyterLab
jupyter lab --version

# Run full test suite
python3 test_setup.py
```

---

**Need help? Check the main README.md or run the test script for detailed diagnostics!**

# 🚀 JupyterLab Quick Start Guide

Get the Qdrant workshop running in JupyterLab in under 5 minutes!

## ⚡ Super Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements-minimal.txt
```

### 2. Set Up Qdrant Cloud
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create free account and cluster
3. Copy your cluster URL and API key

### 3. Configure Environment
```bash
cp env.example .env
# Edit .env with your credentials
```

### 4. Launch JupyterLab
```bash
jupyter lab
```

### 5. Open First Notebook
Navigate to `01_fundamentals.ipynb` and start learning!

## 🔧 Alternative Setup Methods

### Option A: Use the Setup Scripts
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

### Option B: Use the Python Launcher
```bash
python launch_workshop.py
```

### Option C: Manual Setup
```bash
# Install packages
pip install qdrant-client pandas numpy tqdm matplotlib scikit-learn jupyterlab

# Create .env file
cp env.example .env
# Edit .env with your credentials

# Launch JupyterLab
jupyter lab
```

## 🌐 Qdrant Cloud Setup

### Free Tier Details
- **Storage**: 1GB
- **Memory**: 512MB RAM
- **Cost**: $0/month
- **No credit card required**

### Required Credentials
```bash
QDRANT_URL="https://your-cluster.qdrant.io:6333"
QDRANT_API_KEY="your-api-key"
```

## 📚 Notebook Order

Work through the notebooks in this order:

1. **`01_fundamentals.ipynb`** - Basic concepts and operations
2. **`02_hybrid_search.ipynb`** - Dense + sparse vector search
3. **`03_mmr_reranking.ipynb`** - Diversity-aware ranking
4. **`04_hnsw_health.ipynb`** - Performance optimization
5. **`05_agentic_rag.ipynb`** - Intelligent search agents

## 🧪 Test Your Setup

Run the test script to verify everything works:
```bash
python test_setup.py
```

## 🆘 Common Issues

### Import Errors
```bash
pip install -r requirements.txt
```

### Connection Issues
- Check your `.env` file has real credentials
- Verify cluster is running at cloud.qdrant.io
- Ensure internet connectivity

### JupyterLab Won't Start
```bash
pip install --upgrade jupyterlab
jupyter lab --version
```

## 💡 Pro Tips

- **Use the browser console** to see detailed error messages
- **Check the README.md** for comprehensive documentation
- **Start with small datasets** if you have memory constraints
- **Save your work** - notebooks can be long-running

## 🔗 Useful Links

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Discord](https://discord.gg/qdrant)
- [Cloud Dashboard](https://cloud.qdrant.io)

---

**Ready to dive into vector databases? Start with `01_fundamentals.ipynb`! 🚀**

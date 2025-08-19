# 🚀 Qdrant Vector Database Workshop

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![JupyterLab](https://img.shields.io/badge/JupyterLab-4.0+-orange.svg)](https://jupyterlab.readthedocs.io/)
[![Qdrant](https://img.shields.io/badge/Qdrant-1.8+-green.svg)](https://qdrant.tech/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/thierrypdamiba/dsdojo?style=social)](https://github.com/thierrypdamiba/dsdojo)

> **Complete, self-contained workshop on Qdrant vector database fundamentals and advanced techniques. Perfect for JupyterLab environments, workshops, or self-study.**

## 🌟 Features

- ✅ **5 Complete Notebooks** - From basics to advanced agentic RAG
- ✅ **Self-Contained** - No external dependencies beyond Python packages
- ✅ **Cross-Platform** - Works on Linux, Mac, and Windows
- ✅ **Automated Setup** - One-command installation and configuration
- ✅ **Production Ready** - Error handling, validation, and troubleshooting
- ✅ **JupyterLab Optimized** - Perfect for interactive learning

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/thierrypdamiba/dsdojo.git
cd dsdojo
```

### 2. Run Setup (Choose One)
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat

# Or use Python launcher
python3 launch_workshop.py
```

### 3. Configure Qdrant Cloud
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create free account and cluster
3. Edit `.env` file with your credentials

### 4. Launch Workshop
```bash
jupyter lab
```

## 📚 Workshop Content

| Notebook | Topic | Description |
|----------|-------|-------------|
| [01_fundamentals.ipynb](01_fundamentals.ipynb) | 🎯 **Basics** | Collections, vectors, search, filtering |
| [02_hybrid_search.ipynb](02_hybrid_search.ipynb) | 🔀 **Hybrid** | Dense + sparse vector search |
| [03_mmr_reranking.ipynb](03_mmr_reranking.ipynb) | 🎲 **Diversity** | Maximal Marginal Relevance |
| [04_hnsw_health.ipynb](04_hnsw_health.ipynb) | ⚡ **Performance** | HNSW optimization & monitoring |
| [05_agentic_rag.ipynb](05_agentic_rag.ipynb) | 🤖 **Intelligence** | LLM-powered search agents |

## 🛠️ Requirements

- **Python**: 3.8+
- **Package Manager**: pip or conda
- **Internet**: For Qdrant Cloud access
- **Storage**: ~100MB for workshop files

## 📦 Installation Options

### Full Installation (Recommended)
```bash
pip install -r requirements.txt
```

### Minimal Installation
```bash
pip install -r requirements-minimal.txt
```

### Manual Installation
```bash
pip install qdrant-client pandas numpy tqdm matplotlib scikit-learn jupyterlab
```

## 🌐 Qdrant Cloud Setup

### Free Tier Benefits
- **Storage**: 1GB
- **Memory**: 512MB RAM  
- **Cost**: $0/month
- **No credit card required**

### Required Credentials
```bash
QDRANT_URL="https://your-cluster.qdrant.io:6333"
QDRANT_API_KEY="your-api-key"
```

## 🔧 Setup Methods

### Method 1: Automated Setup (Recommended)
```bash
# Linux/Mac
./setup.sh

# Windows  
setup.bat
```

### Method 2: Python Launcher
```bash
python3 launch_workshop.py
```

### Method 3: Manual Setup
```bash
# Install packages
pip install -r requirements-minimal.txt

# Configure environment
cp env.example .env
# Edit .env with your credentials

# Launch JupyterLab
jupyter lab
```

## 🧪 Testing & Verification

### Run Test Suite
```bash
python3 test_setup.py
```

### Expected Results
- ✅ Package imports working
- ✅ Utils module functional  
- ✅ JupyterLab available
- ⚠️ .env configured (after adding real credentials)

## 📖 Documentation

- **[JupyterLab Quick Start](JUPYTERLAB_QUICKSTART.md)** - Get running in 5 minutes
- **[Setup Verification](SETUP_VERIFICATION.md)** - Troubleshooting guide
- **[Summary](SUMMARY.md)** - Complete overview and customization

## 🎯 Use Cases

- **Workshops & Training** - Self-contained, easy distribution
- **Self-Study** - Comprehensive documentation
- **Team Onboarding** - Standardized learning path
- **JupyterLab Environments** - Optimized for notebook workflows

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python3 test_setup.py

# Format code
black *.py
flake8 *.py
```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt
```

**JupyterLab Won't Start**
```bash
pip install --upgrade jupyterlab
```

**Connection Issues**
- Check `.env` file has real credentials
- Verify cluster is running at cloud.qdrant.io
- Ensure internet connectivity

### Getting Help
- Run `python3 test_setup.py` for diagnostics
- Check [Setup Verification](SETUP_VERIFICATION.md) for detailed troubleshooting
- Open an [Issue](https://github.com/thierrypdamiba/dsdojo/issues) on GitHub

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Qdrant](https://qdrant.tech/) - For the amazing vector database
- [JupyterLab](https://jupyterlab.readthedocs.io/) - For the interactive environment
- [FastEmbed](https://github.com/qdrant/fastembed) - For efficient embeddings

## 🔗 Useful Links

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Discord](https://discord.gg/qdrant)
- [Cloud Dashboard](https://cloud.qdrant.io)
- [GitHub Issues](https://github.com/thierrypdamiba/dsdojo/issues)

---

**⭐ Star this repository if you found it helpful!**

**Ready to dive into vector databases? Start with [01_fundamentals.ipynb](01_fundamentals.ipynb)! 🚀**


## Run locally

1. Create and activate a virtual env
```bash
python3 -m venv .venv && source .venv/bin/activate
```

2. Install deps
```bash
pip install -r requirements.txt
```

3. Set environment variables
```bash
export QDRANT_URL=...
export QDRANT_API_KEY=...
export OPENAI_API_KEY=...
```

4. Launch JupyterLab
```bash
python3 -m jupyterlab
```

Each notebook is independent and will create its own collections/data.

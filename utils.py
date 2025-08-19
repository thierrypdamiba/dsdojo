"""
Shared utility functions for Qdrant webinar notebooks
"""
import os
import time
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, SparseVectorParams, SparseVector
try:
    # NamedSparseVector is defined in HTTP models for REST path
    from qdrant_client.http.models.models import NamedSparseVector
except Exception:  # pragma: no cover
    NamedSparseVector = None  # Fallback; will construct tuple for dense only


def get_qdrant_client() -> QdrantClient:
    """Initialize Qdrant client - pre-configured for webinar"""
    # Read credentials strictly from environment variables
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        print("❗ QDRANT_URL and QDRANT_API_KEY must be set. Create a free cluster at https://cloud.qdrant.io and export the variables, e.g.:")
        print('   export QDRANT_URL="https://<your-cluster>.qdrant.io:6333"')
        print('   export QDRANT_API_KEY="<your-api-key>"')
        raise ValueError("Missing required Qdrant credentials in environment")
    else:
        print(f"🌐 Using Qdrant Cloud cluster: {url}")
    
    try:
        return QdrantClient(url=url, api_key=api_key)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. If using your own cluster, verify:")
        print("   - QDRANT_URL format: https://your-cluster.qdrant.io:6333")
        print("   - QDRANT_API_KEY is valid")
        print("3. For help: https://cloud.qdrant.io or Discord: https://discord.gg/qdrant")
        raise


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_config: Union[VectorParams, Dict[str, VectorParams]],
    force_recreate: bool = False
):
    """Create or recreate a collection with the given vector configuration"""
    if force_recreate and client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    if not client.collection_exists(collection_name):
        # Support hybrid collections: split dense and sparse configs if named vectors provided
        vectors_cfg = vector_config
        sparse_vectors_cfg = None

        if isinstance(vector_config, dict):
            dense_cfg: Dict[str, VectorParams] = {}
            sparse_cfg: Dict[str, SparseVectorParams] = {}

            for name, cfg in vector_config.items():
                # Treat VectorParams with size=0 as sparse vector indicator
                if isinstance(cfg, VectorParams) and getattr(cfg, "size", None) == 0:
                    sparse_cfg[name] = SparseVectorParams()
                else:
                    dense_cfg[name] = cfg

            vectors_cfg = dense_cfg if len(dense_cfg) > 0 else None
            sparse_vectors_cfg = sparse_cfg if len(sparse_cfg) > 0 else None

        client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_cfg,
            sparse_vectors_config=sparse_vectors_cfg
        )
        print(f"✓ Created collection '{collection_name}'")
    else:
        print(f"✓ Collection '{collection_name}' already exists")


def create_sample_dataset(size: int = 150, seed: int = 42) -> pd.DataFrame:
    """Create a sample dataset of FAQ/documentation entries"""
    np.random.seed(seed)
    
    categories = ["faq", "howto", "policy", "product", "release"]
    languages = ["en", "es", "fr", "de"]
    
    base_texts = {
        "faq": [
            "How do I reset my password?",
            "What are your business hours?",
            "How can I contact customer support?",
            "What payment methods do you accept?",
            "How do I cancel my subscription?",
            "Is there a mobile app available?",
            "How do I update my account information?",
            "What is your refund policy?",
        ],
        "howto": [
            "How to install the software on Windows",
            "Setting up your development environment",
            "Creating your first project",
            "Configuring database connections",
            "Deploying to production servers",
            "Running automated tests",
            "Setting up monitoring and alerts",
            "Backing up your data regularly",
        ],
        "policy": [
            "Privacy policy and data protection",
            "Terms of service agreement",
            "Cookie usage policy",
            "Data retention guidelines",
            "Security compliance standards",
            "User content moderation rules",
            "Acceptable use policy",
            "Third-party integrations policy",
        ],
        "product": [
            "New feature: Advanced search capabilities",
            "Product overview and key benefits",
            "System requirements and compatibility",
            "Pricing plans and feature comparison",
            "Integration with popular tools",
            "Performance benchmarks and metrics",
            "API documentation and examples",
            "User interface design principles",
        ],
        "release": [
            "Version 2.1 release notes",
            "Bug fixes and improvements",
            "Breaking changes in latest update",
            "New API endpoints available",
            "Performance optimizations implemented",
            "Security patches and updates",
            "Deprecated features announcement",
            "Migration guide for existing users",
        ]
    }
    
    data = []
    for i in range(size):
        category = np.random.choice(categories)
        language = np.random.choice(languages)
        base_text = np.random.choice(base_texts[category])
        
        # Add some variation to text
        variations = [
            base_text,
            f"{base_text} - Updated version",
            f"Learn about {base_text.lower()}",
            f"Guide: {base_text}",
            f"FAQ: {base_text}?"
        ]
        
        text = np.random.choice(variations)
        timestamp = int(time.time()) - np.random.randint(0, 86400 * 365)  # Random time in past year
        
        data.append({
            "id": i + 1,
            "text": text,
            "category": category,
            "lang": language,
            "timestamp": timestamp
        })
    
    return pd.DataFrame(data)


def upsert_points_batch(
    client: QdrantClient,
    collection_name: str,
    df: pd.DataFrame,
    vectors: Union[np.ndarray, Dict[str, np.ndarray]],
    payload_cols: List[str],
    batch_size: int = 100
):
    """Upsert points in batches with progress tracking"""
    from tqdm import tqdm
    
    points = []
    for idx, row in df.iterrows():
        point_vectors = vectors[idx] if isinstance(vectors, np.ndarray) else {k: v[idx] for k, v in vectors.items()}
        payload = {col: row[col] for col in payload_cols}
        
        points.append(PointStruct(
            id=int(row["id"]),
            vector=point_vectors,
            payload=payload
        ))
    
    # Batch upload with progress bar
    for i in tqdm(range(0, len(points), batch_size), desc="Uploading points"):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)


def search_dense(
    client: QdrantClient,
    collection_name: str,
    query_vector: np.ndarray,
    vector_name: str = None,
    limit: int = 10,
    filter_condition: Optional[Filter] = None,
    with_payload: bool = True,
    with_vectors: bool = False,
    score_threshold: Optional[float] = None
):
    """Perform dense vector search"""
    # Normalize query vector format for dense or sparse inputs
    formatted_query_vector: Any
    if hasattr(query_vector, "tolist"):
        # NumPy array or similar
        formatted_query_vector = query_vector.tolist()
    elif isinstance(query_vector, dict):
        # Sparse vector provided as token_id -> weight
        if len(query_vector) > 0:
            sorted_items = sorted(query_vector.items(), key=lambda kv: int(kv[0]) if isinstance(kv[0], str) else kv[0])
            indices = [int(k) for k, _ in sorted_items]
            values = [float(v) for _, v in sorted_items]
        else:
            indices = []
            values = []
        formatted_query_vector = SparseVector(indices=indices, values=values)
    elif hasattr(query_vector, "indices") and hasattr(query_vector, "values"):
        # Already a SparseVector-like object
        formatted_query_vector = query_vector
    else:
        formatted_query_vector = query_vector

    # Use named vectors when vector_name is provided
    # Build named vector appropriately for dense vs sparse
    if vector_name:
        if isinstance(formatted_query_vector, SparseVector) and NamedSparseVector is not None:
            named_or_plain_vector = NamedSparseVector(name=vector_name, vector=formatted_query_vector)
        else:
            named_or_plain_vector = (vector_name, formatted_query_vector)
    else:
        named_or_plain_vector = formatted_query_vector

    search_params = {
        "collection_name": collection_name,
        "query_vector": named_or_plain_vector,
        "limit": limit,
        "with_payload": with_payload,
        "with_vectors": with_vectors
    }
    
    if filter_condition:
        search_params["query_filter"] = filter_condition
    if score_threshold:
        search_params["score_threshold"] = score_threshold
    
    results = client.search(**search_params)
    return results


def search_hybrid_fusion(
    client: QdrantClient,
    collection_name: str,
    dense_vector: np.ndarray,
    sparse_vector: Dict[int, float],
    dense_weight: float = 0.5,
    limit: int = 100,
    final_limit: int = 10,
    filter_condition: Optional[Filter] = None
):
    """Perform hybrid search with client-side score fusion"""
    # Get dense results (named vector)
    dense_results = client.search(
        collection_name=collection_name,
        query_vector=("text_dense", dense_vector.tolist()),
        limit=limit,
        query_filter=filter_condition,
        with_payload=True,
        with_vectors=False
    )
    
    # Get sparse results
    # Normalize sparse vector to SparseVector format
    if len(sparse_vector) > 0:
        sorted_items = sorted(sparse_vector.items(), key=lambda kv: int(kv[0]) if isinstance(kv[0], str) else kv[0])
        s_indices = [int(k) for k, _ in sorted_items]
        s_values = [float(v) for _, v in sorted_items]
    else:
        s_indices, s_values = [], []

    if NamedSparseVector is not None:
        sparse_named = NamedSparseVector(name="text_sparse", vector=SparseVector(indices=s_indices, values=s_values))
    else:
        sparse_named = ("text_sparse", SparseVector(indices=s_indices, values=s_values))

    sparse_results = client.search(
        collection_name=collection_name,
        query_vector=sparse_named,
        limit=limit,
        query_filter=filter_condition,
        with_payload=True,
        with_vectors=False
    )
    
    # Normalize scores and combine
    dense_scores = {r.id: r.score for r in dense_results}
    sparse_scores = {r.id: r.score for r in sparse_results}
    
    # Combine results with weighted fusion
    all_ids = set(dense_scores.keys()) | set(sparse_scores.keys())
    fused_scores = {}
    
    for point_id in all_ids:
        d_score = dense_scores.get(point_id, 0)
        s_score = sparse_scores.get(point_id, 0)
        fused_scores[point_id] = dense_weight * d_score + (1 - dense_weight) * s_score
    
    # Sort by fused score and get top results
    sorted_ids = sorted(fused_scores.keys(), key=lambda x: fused_scores[x], reverse=True)[:final_limit]
    
    # Return results in order
    result_map = {r.id: r for r in (dense_results + sparse_results)}
    fused_results = []
    
    for point_id in sorted_ids:
        if point_id in result_map:
            result = result_map[point_id]
            result.score = fused_scores[point_id]  # Update with fused score
            fused_results.append(result)
    
    return fused_results


def mmr_rerank(
    query_vector: np.ndarray,
    candidate_vectors: np.ndarray,
    candidate_results: List,
    lambda_param: float = 0.5,
    k: int = 10
) -> List:
    """Maximal Marginal Relevance reranking"""
    if len(candidate_results) == 0:
        return []
    
    selected_indices = []
    remaining_indices = list(range(len(candidate_results)))
    
    # Normalize vectors for cosine similarity
    query_norm = query_vector / np.linalg.norm(query_vector)
    candidates_norm = candidate_vectors / np.linalg.norm(candidate_vectors, axis=1, keepdims=True)
    
    # Start with most relevant
    relevance_scores = np.dot(candidates_norm, query_norm)
    first_idx = np.argmax(relevance_scores)
    selected_indices.append(first_idx)
    remaining_indices.remove(first_idx)
    
    # Iteratively select based on MMR score
    for _ in range(min(k - 1, len(remaining_indices))):
        mmr_scores = []
        
        for idx in remaining_indices:
            # Relevance score
            relevance = relevance_scores[idx]
            
            # Max similarity to already selected
            max_sim = 0
            for sel_idx in selected_indices:
                sim = np.dot(candidates_norm[idx], candidates_norm[sel_idx])
                max_sim = max(max_sim, sim)
            
            # MMR score
            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim
            mmr_scores.append((idx, mmr_score))
        
        # Select best MMR score
        best_idx = max(mmr_scores, key=lambda x: x[1])[0]
        selected_indices.append(best_idx)
        remaining_indices.remove(best_idx)
    
    return [candidate_results[i] for i in selected_indices]


def exact_topk(
    query_vector: np.ndarray,
    all_vectors: np.ndarray,
    k: int = 10
) -> List[Tuple[int, float]]:
    """Compute exact top-k using brute force cosine similarity"""
    # Normalize vectors
    query_norm = query_vector / np.linalg.norm(query_vector)
    all_norm = all_vectors / np.linalg.norm(all_vectors, axis=1, keepdims=True)
    
    # Compute cosine similarities
    similarities = np.dot(all_norm, query_norm)
    
    # Get top-k indices and scores
    top_indices = np.argsort(similarities)[::-1][:k]
    top_scores = similarities[top_indices]
    
    return [(int(idx), float(score)) for idx, score in zip(top_indices, top_scores)]


def measure_latency(func, n_runs: int = 100) -> Dict[str, float]:
    """Measure function latency statistics"""
    times = []
    for _ in range(n_runs):
        start = time.time()
        func()
        end = time.time()
        times.append((end - start) * 1000)  # Convert to milliseconds
    
    times = np.array(times)
    return {
        "p50": np.percentile(times, 50),
        "p95": np.percentile(times, 95),
        "p99": np.percentile(times, 99),
        "mean": np.mean(times),
        "std": np.std(times)
    }


def calculate_recall_at_k(predicted: List[int], ground_truth: List[int], k: int = 10) -> float:
    """Calculate recall@k between predicted and ground truth results"""
    pred_set = set(predicted[:k])
    truth_set = set(ground_truth[:k])
    
    if len(truth_set) == 0:
        return 0.0
    
    intersection = len(pred_set.intersection(truth_set))
    return intersection / len(truth_set)


def calculate_redundancy(texts: List[str], vectors: np.ndarray = None) -> float:
    """Calculate redundancy score (mean pairwise similarity) for a result set"""
    if vectors is not None and len(vectors) > 1:
        # Use vector similarities if available
        norm_vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        similarities = np.dot(norm_vectors, norm_vectors.T)
        # Get upper triangle (excluding diagonal)
        upper_triangle = np.triu(similarities, k=1)
        non_zero_similarities = upper_triangle[upper_triangle > 0]
        return np.mean(non_zero_similarities) if len(non_zero_similarities) > 0 else 0.0
    else:
        # Simple text-based redundancy (placeholder)
        if len(texts) < 2:
            return 0.0
        # Count word overlaps as a simple proxy
        words_sets = [set(text.lower().split()) for text in texts]
        similarities = []
        for i in range(len(words_sets)):
            for j in range(i + 1, len(words_sets)):
                intersection = len(words_sets[i].intersection(words_sets[j]))
                union = len(words_sets[i].union(words_sets[j]))
                sim = intersection / union if union > 0 else 0
                similarities.append(sim)
        return np.mean(similarities) if similarities else 0.0


def print_search_results(results, title: str = "Search Results", max_results: int = 5):
    """Pretty print search results"""
    print(f"\n{title}")
    print("=" * len(title))
    
    for i, result in enumerate(results[:max_results]):
        print(f"\n{i+1}. Score: {result.score:.4f}")
        print(f"   ID: {result.id}")
        if result.payload:
            print(f"   Category: {result.payload.get('category', 'N/A')}")
            print(f"   Language: {result.payload.get('lang', 'N/A')}")
            print(f"   Text: {result.payload.get('text', 'N/A')[:100]}...")


def create_payload_index(client: QdrantClient, collection_name: str, field_name: str, field_type: str = "keyword"):
    """Create a payload index for faster filtering"""
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_type=field_type
        )
        print(f"✓ Created payload index for '{field_name}' ({field_type})")
    except Exception as e:
        print(f"Note: Index for '{field_name}' may already exist: {e}")


def print_system_info():
    """Print system and library version information"""
    import sys
    
    print("🔧 System Information:")
    print(f"   Python: {sys.version.split()[0]}")
    
    # Check core dependencies
    deps = [
        ("qdrant_client", "Qdrant Client", "qdrant-client"),
        ("numpy", "NumPy", "numpy"),
        ("pandas", "Pandas", "pandas"),
        ("matplotlib", "Matplotlib", "matplotlib"),
        ("sklearn", "Scikit-learn", "scikit-learn")
    ]
    
    for import_name, display_name, pip_name in deps:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {display_name}: {version}")
        except ImportError:
            print(f"   ❌ {display_name}: not installed (run: pip install {pip_name})")
    
    # Check optional dependencies
    optional_deps = [
        ("fastembed", "FastEmbed", "fastembed"),
        ("openai", "OpenAI", "openai"),
        ("anthropic", "Anthropic", "anthropic")
    ]
    
    print("\n🔧 Optional Dependencies:")
    for import_name, display_name, pip_name in optional_deps:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {display_name}: {version}")
        except ImportError:
            print(f"   ⚪ {display_name}: not installed (optional)")
    
    # JupyterLab specific info
    try:
        import IPython
        if IPython.get_ipython() is not None:
            print(f"\n🔬 Environment: JupyterLab/Notebook detected")
        else:
            print(f"\n🔬 Environment: Python script")
    except ImportError:
        print(f"\n🔬 Environment: Standard Python")

def install_missing_packages():
    """Install missing core packages - JupyterLab friendly"""
    import subprocess
    import sys
    
    core_packages = [
        ("qdrant-client", "qdrant_client"),
        ("pandas", "pandas"), 
        ("numpy", "numpy"),
        ("tqdm", "tqdm"),
        ("matplotlib", "matplotlib"),
        ("scikit-learn", "sklearn")
    ]
    
    print("🔧 Checking core dependencies...")
    missing = []
    
    for pip_name, import_name in core_packages:
        try:
            __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name} - needs installation")
            missing.append(pip_name)
    
    if missing:
        print(f"\n📦 Installing {len(missing)} missing packages...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--quiet"
            ] + missing)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Installation failed: {e}")
            print("Please install manually with:")
            print(f"   pip install {' '.join(missing)}")
    else:
        print("✅ All core dependencies satisfied!")
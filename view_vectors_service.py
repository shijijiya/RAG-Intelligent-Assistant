# view_vectors_via_service.py
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

def view_vectors():
    # 创建向量存储服务
    service = VectorStoreService(
        DashScopeEmbeddings(model=config.embedding_model_name)
    )
    
    # 获取底层的 Chroma 集合
    collection = service.vector_store._client.get_collection(
        config.collection_name
    )
    
    # 统计总数
    count = collection.count()
    print(f"向量库中总共有 {count} 个向量")
    
    if count > 0:
        # 获取所有数据
        results = collection.get(
            include=["documents", "metadatas", "embeddings"]
        )
        
        documents = results['documents']
        metadatas = results['metadatas']
        embeddings = results['embeddings']
        
        for i, (doc, meta, emb) in enumerate(zip(documents, metadatas, embeddings)):
            print(f"\n【第 {i+1} 个向量】")
            print(f"📄 文档内容：{doc[:200]}{'...' if len(doc) > 200 else ''}")
            print(f"📝 元数据：{meta}")
            print(f"🔢 向量维度：{len(emb)}")
            print(f"📊 向量前 10 个值：{emb[:10]}")
            print(f"📊 向量后 10 个值：{emb[-10:]}")
            print(f"ℹ️  向量统计 - 最小值：{min(emb):.6f}, 最大值：{max(emb):.6f}, 平均值：{sum(emb)/len(emb):.6f}")

if __name__ == '__main__':
    view_vectors()
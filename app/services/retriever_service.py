from supabase import create_client

class RetrieverService:

    def __init__(self, supabase_url: str, supabase_key: str):
        self.client = create_client(supabase_url, supabase_key)

    def search(self, embedding, match_count: int = 5):
        response = self.client.rpc("match_embeddings", {
            "query_embedding": embedding,
            "match_count": match_count
        }).execute()
        
        return response.data
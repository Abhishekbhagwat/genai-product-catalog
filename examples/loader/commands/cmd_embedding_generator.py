from model import parse_nlp_description

class EmbeddingGeneratorCommand:
    @staticmethod
    def generate_embeddings(description: str):
        return parse_nlp_description(description)
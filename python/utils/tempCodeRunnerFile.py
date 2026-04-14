response = client.feature_extraction(
        texts,
        model="BAAI/bge-base-en"
    )
    return {"
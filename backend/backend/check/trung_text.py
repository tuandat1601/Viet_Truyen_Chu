from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text_vietnamese(text):
    # Tiền xử lý văn bản tiếng Việt
    tokenized_text = ViTokenizer.tokenize(text)
    # Các bước tiền xử lý khác (loại bỏ stopwords, chuẩn hóa văn bản, ...)

    return tokenized_text

def calculate_similarity(text1, text2):
    # Tiền xử lý văn bản
    preprocessed_text1 = preprocess_text_vietnamese(text1)
    preprocessed_text2 = preprocess_text_vietnamese(text2)

    # Biểu diễn văn bản dưới dạng vector TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

    # Tính toán Cosine Similarity giữa hai vector văn bản
    cosine_similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return cosine_similarity_score

# Sử dụng chương trình kiểm duyệt truyện
new_story = "Nội dung truyện mới"
existing_story = "Nội dung truyện mới"

similarity = calculate_similarity(new_story, existing_story)
print(f"Truyện bị trùng {round(similarity * 100,2)}% với truyện trong kho truyện.")
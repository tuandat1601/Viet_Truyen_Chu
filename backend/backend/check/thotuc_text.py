from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
# Dữ liệu huấn luyện
def checkthotuc():
    sentences = ["This is a clean sentence.",
             "This is a sentence with offensive words.",
             "I don't like using bad language in my speech.",
             "Please refrain from using inappropriate language.",
             "ditme",
             "dit",
             "dm"
         ]

    labels = [0, 1, 0, 0,1,1,1]  # 0: Không có từ ngữ thô tục, 1: Có từ ngữ thô tục

# Xây dựng pipeline
    pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),  # Chuyển đổi văn bản thành ma trận đếm từ
    ('classifier', MultinomialNB())  # Sử dụng mô hình Naive Bayes
])

# Huấn luyện mô hình
    pipeline.fit(sentences, labels)

# Lưu mô hình vào file
    
    joblib.dump(pipeline, 'model.pkl')
    pipeline = joblib.load('model.pkl')

# Dữ liệu mới cần dự đoán
    new_sentences = ["dmm nó"
         ]

# Dự đoán nhãn cho dữ liệu mới
    predictions = pipeline.predict(new_sentences)

# In kết quả dự đoán
    for sentence, prediction in zip(new_sentences, predictions):
        if prediction == 0:
            print(f"'{sentence}' không có từ ngữ thô tục.")
        else:
            print(f"'{sentence}' chứa từ ngữ thô tục.")
checkthotuc()
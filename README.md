Hướng dẫn cài đặt và chạy

Bước 1: Chuẩn bị mã nguồn
git clone https://github.com/Ngoenngoen1910/mini-travel
cd streamlit-chat
pip install -r requirements.txt

Bước 2: Cấu hình Firebase
Tạo thư mục .streamlit và file .streamlit/secrets.toml với cấu trúc sau để kết nối database:
[firebase_client]
apiKey = "..."
authDomain = "..."
projectId = "..."
storageBucket = "..."
messagingSenderId = "..."
appId = "..."
# Lấy từ Firebase Console -> Project Settings -> General -> Your apps

[firebase_admin]
type = "..."
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "..."
token_uri = "..."
auth_provider_x509_cert_url = "..."
client_x509_cert_url = "..."
universe_domain = "..."
# Lấy từ file JSON khi tạo Service Account trong Firebase Console

Bước 3: Khởi chạy AI Server trên Google Colab
Truy cập notebook Colab tại đây: https://colab.research.google.com/drive/1PkBY4oR9MsHk9gKY6FurzHN8A6HFZTti?usp=sharing
Chạy tất cả theo hướng dẫn bên trong để cài đặt Ollama trên Colab
Đợi quá trình chạy hoàn tất, lấy link Pinggy
# LƯU Ý: Giữ tab Google Colab luôn mở trong quá trình sử dụng

Bước 4: Kết nối và Chạy ứng dụng
Mở file app.py trên máy
Tìm dòng OLLAMA_HOST và thay thế bằng link Pinggy bạn vừa lấy được
Khởi chạy Streamlit:
streamlit run app.py
Truy cập http://localhost:8501 hoặc URL được tạo

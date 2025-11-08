# Hướng dẫn cài đặt và chạy

# Bước 1: Chuẩn bị mã nguồn
git clone https://github.com/Ngoenngoen1910/mini-travel

cd streamlit-chat

pip install -r requirements.txt

# Bước 2: Cấu hình Firebase

Tạo thư mục .streamlit và file .streamlit/secrets.toml với file secrets.toml đi kèm

# Bước 3: Khởi chạy AI Server trên Google Colab

Truy cập: https://colab.research.google.com/drive/1PkBY4oR9MsHk9gKY6FurzHN8A6HFZTti?usp=sharing

Chạy tất cả các cell bên trong để cài đặt Ollama trên Colab.

Ở cell 3 sau khi chạy thì chạy lệnh dưới để tunnel ra bên ngoài

ssh -p 443 -R0:localhost:11434 qr@a.pinggy.io

Đợi quá trình chạy hoàn tất, lấy link Pinggy và thay thế trong cell 4

LƯU Ý: Giữ tab Google Colab luôn mở trong quá trình sử dụng

# Bước 4: Kết nối và Chạy ứng dụng

Mở file app.py trên máy

Tìm dòng OLLAMA_HOST và thay thế bằng link Pinggy vừa lấy được

Khởi chạy Streamlit:

streamlit run app.py

Truy cập http://localhost:8501 hoặc URL được tạo

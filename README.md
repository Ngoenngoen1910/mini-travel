# Hướng dẫn cài đặt và chạy

# Bước 1: Tải Git và chuẩn bị mã nguồn

Nếu chưa có, tải và cài đặt Git từ https://git-scm.com/download/

Mở terminal và chạy các lệnh sau:
```bash
git clone https://github.com/Ngoenngoen1910/mini-travel
cd streamlit-chat
pip install -r requirements.txt__
```
# Bước 2: Cấu hình Firebase

Truy cập Firebase Console

Nhấn Add project, đặt tên

Trong menu bên trái, chọn Build:

Authentication > Get started > Chọn Email/Password > Enable > Save.

Firestore Database > Create database > Start > Next > Enable.

# Bước 3: Khởi chạy Ollama trên Google Colab

Truy cập: https://colab.research.google.com/drive/1PkBY4oR9MsHk9gKY6FurzHN8A6HFZTti?usp=sharing

Chạy tất cả các cell bên trong để cài đặt Ollama trên Colab.

Ở cell 3 sau khi chạy thì chạy lệnh dưới để tunnel ra bên ngoài
```bash
ssh -p 443 -R0:localhost:11434 qr@a.pinggy.io
```
Đợi quá trình chạy hoàn tất, lấy link Pinggy và thay thế trong cell 4
```bash
# Thay "http://localhost:11434" bằng link sinh ra từ pingy.io, ví dụ nếu thấy "http://bsqlv-34-125-123-92.a.free.pinggy.link"
!curl http://lpdvq-34-83-254-107.a.free.pinggy.link/api/generate -d '{ "model": "llama3", "prompt": "Tell me a joke", "stream": false}'
```
LƯU Ý: Giữ tab Google Colab luôn mở trong quá trình sử dụng

# Bước 4: Kết nối và Chạy ứng dụng

Mở file app.py trên máy

Tìm dòng OLLAMA_HOST và thay thế bằng link Pinggy vừa lấy được
```bash
# CẬP NHẬP LINK PINGGY
OLLAMA_HOST = 'http://vlsqc-34-87-72-82.a.free.pinggy.link' <-Thay thế link trong này
client = Client(host=OLLAMA_HOST)
```

Khởi chạy Streamlit:
``` bash
streamlit run app.py
```
Truy cập http://localhost:8501 hoặc URL được tạo

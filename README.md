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

### Tạo cấu hình
Truy cập Firebase Console

Nhấn Add project, đặt tên

Trong menu bên trái, chọn Build:

Authentication > Get started > Email/Password > Enable > Save

Firestore Database > Create database > Start > Next > Enable

Realtime Database > Create database > Database options > asia-southeast1 > Next > Security rules > Start in locked mode > Enable

### Lấy Key 1: [firebase_client]

Nhấn Project Settings ở góc trên bên trái

Trong tab General, cuộn xuống phần Your apps

Nhấn vào biểu tượng Web (</>)

Đặt tên và nhấn Register app

Firebase sẽ hiển thị firebaseConfig. Copy phần có nội dung sau:
```bash
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  databaseURL: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "...",
  measurementId: "..."
}
```

### Lấy Key 2: [firebase_admin]

Trong Project Settings > Service accounts > Generate new private key

Một file .json sẽ được tải về. Mở file và copy toàn bộ


### Tạo file secrets.toml

Tại thư mục streamlit-chat, tạo thư mục .streamlit

Bên trong thư mục .streamlit, tạo file secrets.toml

Dán các khóa key vào file secrets.toml với định đạng được chỉnh như sau:

```bash
[firebase_client]
"apiKey" = "..."
"authDomain" = "..."
"projectId" = "..."
"storageBucket" = "..."
"messagingSenderId" = "..."
"appId" = "..."

[firebase_admin]
"type" = "..."
"project_id" = "..."
"private_key_id" = "..."
"private_key" = "..."
"client_email" = "..."
"client_id" = "..."
"auth_uri" = "..."
"token_uri" = "..."
"auth_provider_x509_cert_url" = "..."
"client_x509_cert_url" = "..."
"universe_domain" = "..."
```

# Bước 3: Khởi chạy Ollama trên Google Colab

Truy cập: https://colab.research.google.com/drive/1PkBY4oR9MsHk9gKY6FurzHN8A6HFZTti?usp=sharing

Chạy tất cả các cell bên trong để cài đặt Ollama trên Colab

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

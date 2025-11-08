import time
import streamlit as st
import pyrebase
import firebase_admin
import requests
from firebase_admin import credentials, firestore, auth as admin_auth
from collections import deque
from datetime import datetime, timezone
from ollama import Client
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Mini Travel", page_icon="✈️", layout="wide")

MODEL = "llama3.2:1b"
# CẬP NHẬP LINK PINGGY
OLLAMA_HOST = 'http://vlsqc-34-87-72-82.a.free.pinggy.link'
client = Client(host=OLLAMA_HOST)

@st.cache_resource
def get_firebase_clients():
    firebase_cfg = st.secrets["firebase_client"]
    firebase_app = pyrebase.initialize_app(firebase_cfg)
    auth_pyrebase = firebase_app.auth()

    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_admin"]))
        firebase_admin.initialize_app(cred)
    db_firestore = firestore.client()
    return auth_pyrebase, db_firestore

try:
    auth, db = get_firebase_clients()
except Exception as e:
    st.error(f"Lỗi kết nối Firebase. Kiểm tra secrets.toml. Chi tiết: {e}")
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = deque([], maxlen=20) 

def save_message_to_firestore(uid: str, role: str, content: str):
    """Lưu tin nhắn (hoặc lịch trình) vào subcollection của user"""
    doc = {
        "role": role,
        "content": content,
        "ts": datetime.now(timezone.utc)
    }
    db.collection("users").document(uid).collection("travel_history").add(doc)

def load_history_from_firestore(uid: str, limit: int = 20):
    """Tải lịch sử cũ khi đăng nhập lại"""
    q = (db.collection("users").document(uid)
         .collection("travel_history")
         .order_by("ts", direction=firestore.Query.DESCENDING)
         .limit(limit))
    docs = list(q.stream())
    docs.reverse()
    out = []
    for d in docs:
        data = d.to_dict()
        out.append({"role": data.get("role"), "content": data.get("content")})
    return out

def generate_itinerary(payload: dict):
    """Tạo prompt và gọi Ollama để sinh lịch trình"""
    
    prompt = f"""
    Đóng vai trò là một chuyên gia lập kế hoạch du lịch địa phương, cực kỳ thông thạo và logic.
    Nhiệm vụ của bạn là tạo một lịch trình du lịch, thực tế, và hấp dẫn bằng Tiếng Việt.

    THÔNG TIN ĐẦU VÀO:
    - Nơi xuất phát (Điểm bắt đầu): {payload['origin']}
    - Nơi đến (Điểm chính của kỳ nghỉ): {payload['destination']}
    - Tổng số ngày nghỉ: {payload['num_days']} ngày (Từ Ngày 1 đến Ngày {payload['num_days']})
    - Sở thích: {', '.join(payload['interests'])}
    - Nhịp độ: {payload['pace']}

    QUY TẮC BẮT BUỘC (TUYỆT ĐỐI KHÔNG VI PHẠM):

    1.  **QUAN TRỌNG NHẤT - LOGIC CHUYẾN ĐI:**
        -   Lịch trình du lịch {payload['num_days']} ngày này phải diễn ra **TẠI {payload['destination']}** và các khu vực lân cận (ví dụ: đi Hội An từ Đà Nẵng).
        -   **{payload['origin']}** CHỈ LÀ nơi người dùng bắt đầu. TUYỆT ĐỐI KHÔNG được đưa các hoạt động tham quan tại **{payload['origin']}** vào lịch trình kỳ nghỉ. Toàn bộ lịch trình (Ngày 1, Ngày 2,...) là ở **{payload['destination']}**.
        -   Ví dụ: Nếu đi từ Hà Nội đến Đà Nẵng, thì Ngày 1 phải bắt đầu ở Đà Nẵng, chứ không phải Hà Nội.

    2.  **LOGIC ĐỊA LÝ:**
        -   Các địa điểm tham quan trong một buổi (Sáng/Chiều/Tối) phải ở gần nhau, thuận tiện di chuyển. Không được sắp xếp lung tung (ví dụ: buổi sáng ở Bà Nà, buổi chiều chạy ra Sơn Trà rồi tối lại quay vào trung tâm).
        -   Phải đảm bảo tên địa danh, địa chỉ là CÓ THẬT và CHÍNH XÁC tại {payload['destination']}.

    YÊU CẦU ĐỊNH DẠNG ĐẦU RA:

    1.  **Ngôn ngữ:** 100% Tiếng Việt.
    2.  **Cấu trúc:** Bắt đầu ngay lập tức với "Ngày 1:", tiếp theo là "Ngày 2:",... cho đến hết "Ngày {payload['num_days']}:".
    3.  **Chi tiết:** Mỗi ngày phải chia rõ ràng 3 buổi:
        -   Sáng : [Hoạt động]
        -   Chiều : [Hoạt động]
        -   Tối : [Hoạt động]
    4.  **Giải thích:** Sau mỗi hoạt động hoặc cuối mỗi buổi, phải có một "Lời giải thích ngắn gọn:" (ví dụ: "Lời giải thích ngắn gọn: Nơi này rất hợp cho sở thích {payload['interests']} vì...")
    5.  **Tối giản:** KHÔNG viết lời chào mở đầu hoặc câu kết luận. Chỉ tập trung vào lịch trình.
    """

    try:
        response = client.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"⚠️ Lỗi kết nối đến Travel AI Agent: {e}. Vui lòng kiểm tra lại đường truyền hoặc server Ollama."

def auth_ui():
    st.title("🌏 Mini Travel")
    
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký mới"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Mật khẩu", type="password", key="login_pass")
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
            
            if submitted:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.user = {"uid": user["localId"], "email": email, "idToken": user["idToken"]}
                    
                    # Tải lịch sử cũ
                    history = load_history_from_firestore(user["localId"])
                    st.session_state.messages = deque(history, maxlen=20)
                    
                    st.success("Đăng nhập thành công!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Đăng nhập thất bại: {e}")

    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("Mật khẩu (tối thiểu 6 ký tự)", type="password", key="signup_pass")
            submitted_signup = st.form_submit_button("Tạo tài khoản", use_container_width=True)
            
            if submitted_signup:
                try:
                    auth.create_user_with_email_and_password(new_email, new_pass)
                    st.success("Tạo tài khoản thành công! Vui lòng chuyển qua tab Đăng nhập.")
                except Exception as e:
                    st.error(f"Đăng ký thất bại: {e}")

def main_app_ui():
    col_header_1, col_header_2 = st.columns([8, 1])
    with col_header_1:
        st.subheader(f"Chào mừng, {st.session_state.user['email']}!")
    with col_header_2:
        if st.button("Đăng xuất", type="primary"):
            st.session_state.user = None
            st.session_state.messages.clear()
            st.rerun()
    
    st.divider()

    left_col, right_col = st.columns([1, 1.5], gap="large")

    with left_col:
        st.markdown("### Thiết lập chuyến đi")
        with st.container(border=True):
            with st.form("trip_form"):
                c1, c2 = st.columns(2)
                origin = c1.text_input("Điểm đi", placeholder="VD: Ha Noi")
                destination = c2.text_input("Điểm đến", placeholder="VD: Ho Chi Minh")
                
                dates = st.date_input("Thời gian", [])
                
                interests = st.multiselect(
                    "Sở thích",
                    ["🍜 Ẩm thực", "🏛️ Bảo tàng & Lịch sử", "🌳 Thiên nhiên", "🍷 Cuộc sống về đêm"],
                    default=["🍜 Ẩm thực", "🌳 Thiên nhiên"]
                )
                
                pace = st.radio(
                    "Nhịp độ chuyến đi",
                    ["😌 Thư giãn", "🙂 Bình thường", "🏃 Bận rộn"],
                    horizontal=True,
                    index=1
                )
                
                submitted = st.form_submit_button("Lập kế hoạch ngay", use_container_width=True)

                if submitted:
                    if not origin or not destination:
                        st.error("Vui lòng nhập đủ Điểm đi và Điểm đến.")
                    elif len(dates) != 2:
                        st.error("Vui lòng chọn đủ Ngày bắt đầu và Ngày kết thúc trên lịch.")
                    else:
                        delta = dates[1] - dates[0]
                        num_days = delta.days + 1
                        
                        date_str = f"{dates[0].strftime('%d/%m/%Y')} - {dates[1].strftime('%d/%m/%Y')}"
                        
                        payload = {
                            "origin": origin,
                            "destination": destination,
                            "dates": date_str,
                            "num_days": num_days, 
                            "interests": interests,
                            "pace": pace
                        }
                        
                        user_msg = f"**Yêu cầu chuyến đi:** {origin} ➡️ {destination} | 📅 {date_str} ({num_days} ngày) | {', '.join(interests)} | {pace}"
                        st.session_state.messages.append({"role": "user", "content": user_msg})
                        save_message_to_firestore(st.session_state.user["uid"], "user", user_msg)

                        with st.spinner(f"AI đang thiết kế lịch trình (khoảng 30s ⏳)"):
                            ai_response = generate_itinerary(payload)
                        
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        save_message_to_firestore(st.session_state.user["uid"], "assistant", ai_response)
                        st.rerun() 

    with right_col:
        st.markdown("###    Lịch trình & Lịch sử")
        
        history_container = st.container(height=700, border=False)
        with history_container:
            if len(st.session_state.messages) == 0:
                st.info("Chưa có lịch trình nào. Hãy điền thông tin bên trái để bắt đầu!")
            else:
                for msg in reversed(list(st.session_state.messages)):
                    if msg["role"] == "user":
                        with st.chat_message("user", avatar="🧑‍💻"):
                            st.markdown(msg["content"])
                    else:
                        with st.chat_message("assistant", avatar="🤖"):
                            with st.expander("Xem chi tiết lịch trình", expanded=True):
                                st.markdown(msg["content"])

if not st.session_state.user:
    auth_ui()
else:
    main_app_ui()

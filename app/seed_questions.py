import requests

BASE_URL = "http://127.0.0.1:8000"
EXAM_CODE_ID  = 1

# Đăng nhập lấy token
resp = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "khanh",  # username bạn vừa dùng
    "password": "123456789", # đổi lại đúng password của bạn
})
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Tạo 40 câu, đáp án luân phiên A/B/C/D
answers = ["A", "B", "C", "D"] * 10
for i, ans in enumerate(answers, start=1):
    r = requests.post(f"{BASE_URL}/questions/", json={
        "exam_code_id": EXAM_CODE_ID,
        "order":   i,
        "correct_answer": ans,
        "score":   1,
    }, headers=headers)
    print(f"Câu {i:2d}: {r.status_code} — đáp án {ans}")
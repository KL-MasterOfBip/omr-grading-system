import requests
import sys

# Khắc phục lỗi in tiếng Việt trên terminal Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def seed_all():
    print("=== BẮT ĐẦU SEED DỮ LIỆU ===")
    
    # 1. Đăng ký tài khoản (nếu chưa có)
    print("\n1. Đăng ký tài khoản...")
    user_data = {
        "username": "khanh",
        "email": "khanh@example.com",
        "password": "123456789",
        "full_name": "Giáo viên Khánh"
    }
    r_reg = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if r_reg.status_code == 201:
        print(" -> Đăng ký thành công!")
    elif r_reg.status_code == 400:
        print(" -> Tài khoản đã tồn tại, tiếp tục đăng nhập.")
    else:
        print(f" -> Lỗi đăng ký: {r_reg.text}")
        return

    # 2. Đăng nhập lấy token
    print("\n2. Đăng nhập lấy token...")
    r_login = requests.post(f"{BASE_URL}/auth/login", data={
        "username": "khanh",
        "password": "123456789",
    })
    if r_login.status_code != 200:
        print(f" -> Lỗi đăng nhập: {r_login.text}")
        return
    token = r_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(" -> Đăng nhập thành công!")

    # 3. Tạo Exam (Bài thi)
    print("\n3. Tạo Bài thi mới...")
    exam_data = {
        "title": "Kỳ thi Khảo sát Chất lượng Toán 12",
        "description": "Bài thi trắc nghiệm 40 câu",
        "subject": "Toán",
        "num_questions": 40,
        "num_choices": 4
    }
    r_exam = requests.post(f"{BASE_URL}/exams/", json=exam_data, headers=headers)
    if r_exam.status_code != 201:
        print(f" -> Lỗi tạo Exam: {r_exam.text}")
        return
    exam_id = r_exam.json()["id"]
    print(f" -> Tạo bài thi thành công (exam_id = {exam_id})")

    # 4. Tạo ExamCode (Mã đề)
    print("\n4. Tạo Mã đề 101...")
    code_data = {
        "exam_id": exam_id,
        "code": "101",
        "description": "Mã đề gốc"
    }
    r_code = requests.post(f"{BASE_URL}/exam-codes/", json=code_data, headers=headers)
    if r_code.status_code != 201:
        print(f" -> Lỗi tạo ExamCode: {r_code.text}")
        return
    exam_code_id = r_code.json()["id"]
    print(f" -> Tạo Mã đề thành công (exam_code_id = {exam_code_id})")

    # 5. Tạo Câu hỏi (Questions)
    print("\n5. Tạo 40 câu hỏi mẫu (đáp án luân phiên A/B/C/D)...")
    answers = ["A", "B", "C", "D"] * 10
    success_count = 0
    for i, ans in enumerate(answers, start=1):
        r_q = requests.post(f"{BASE_URL}/questions/", json={
            "exam_code_id": exam_code_id,
            "order": i,
            "correct_answer": ans,
            "score": 1,
        }, headers=headers)
        
        if r_q.status_code == 201:
            success_count += 1
        else:
            print(f" -> Lỗi tạo câu {i}: {r_q.text}")
            
    print(f" -> Tạo thành công {success_count}/40 câu hỏi!")
    print("\n=== HOÀN TẤT SEED ===")

if __name__ == "__main__":
    seed_all()

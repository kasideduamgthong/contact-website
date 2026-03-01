# Contact Website

เว็บไซต์ Portfolio และระบบจัดการข้อมูลติดต่อ (Contact Management System) พัฒนาด้วย Flask และ Bootstrap 5

---
## ความสามารถของระบบ

- พัฒนาโดยใช้ Flask Framework
- ออกแบบ Responsive ด้วย Bootstrap 5
- ใช้ SQLite Database ผ่าน SQLAlchemy ORM
- ระบบ Contact Form (บันทึกข้อมูลลงฐานข้อมูล)
- ระบบ Blog (เพิ่ม / แก้ไข / ลบ / แสดงผล)
- ระบบ Testimonials
- ระบบ Admin Login (Session-based Authentication)
- หน้า Dashboard สำหรับผู้ดูแลระบบ
- ระบบลบข้อความจากหน้า Dashboard
- ป้องกันหน้า Dashboard สำหรับผู้ใช้ทั่วไป

---

## หน้าต่าง ๆ ภายในเว็บไซต์

1. Home  
2. About  
3. Services  
4. Portfolio  
5. Portfolio Detail  
6. Contact  
7. Blog  
8. Blog Detail  
9. Add Blog (Admin)  
10. Edit Blog (Admin)  
11. Dashboard (Admin Only)  
12. Testimonials  
13. Admin Login  

---


## ⚙ วิธีติดตั้งและใช้งาน

### 1.Clone Repository

```bash
git clone <your-repository-url>
cd contact-website

2. สร้าง Virtual Environment
python -m venv venv

3. ติดตั้ง Dependencies
pip install -r requirements.txt

วิธีรันโปรแกรม
python app.py

เปิดเบราว์เซอร์ไปที่:
http://127.0.0.1:5000
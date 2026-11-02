# การทดสอบ QuickPizza API ด้วย pytest และ requests

Repository นี้ประกอบด้วยชุดทดสอบอัตโนมัติ (Automated API Test Suites) สำหรับทดสอบระบบ **QuickPizza** (`https://quickpizza.grafana.com`) ซึ่งเป็นส่วนหนึ่งของใบงานปฏิบัติการรายวิชา ITDS362 Software Quality Assurance and Testing

---

## 1. การติดตั้งและการตั้งค่าระบบ (Installation and Setup)

### สิ่งที่จำเป็นต้องมี (Prerequisites)
- Python 3.10 ขึ้นไป
- `curl` หรือ `curl.exe`

### การสร้าง Virtual Environment และติดตั้ง Packages
ทำการ Clone repository นี้ และสร้าง virtual environment:

```powershell
# บน Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

บน macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. การรันชุดทดสอบ (Running Tests)

### รันการทดสอบทั้งหมดพร้อมแสดงรายละเอียด:
```powershell
pytest -v
```

### รันการทดสอบและสร้างรายงาน HTML Report:
```powershell
pytest -v --html=report.html --self-contained-html
```

### ผลลัพธ์ที่คาดหวัง (Expected Results)
- **32 passed, 1 xfailed**
- โดย 1 เคสที่เป็น `xfailed` คือเคสที่บันทึกบั๊กของระบบ QuickPizza ซึ่งตอบกลับด้วย HTTP 500 แทนที่จะเป็น HTTP 400 เมื่อลูกค้าตัดเครื่องมือทำพิซซ่าออกทั้งหมด

---

## 3. แบบจำลองขอบเขตอินพุต (Input Domain Model) สำหรับ `POST /api/ratings`

ตารางนี้แสดงการแบ่ง Input Space Partitioning และการครอบคลุมแบบ **Base Choice Coverage (BCC)** สำหรับการสร้างเรตติ้ง (`POST /api/ratings`):

| คุณลักษณะ (Characteristic) | บล็อก (Blocks) | ค่าที่ใช้ในการทดสอบ (Values) | ฟังก์ชันทดสอบที่ครอบคลุม (Test Function) |
| :--- | :--- | :--- | :--- |
| **C1 Value of stars**<br>(ค่าคะแนนดาว) | ต่ำกว่า 1<br>**1 ถึง 5 (Base)**<br>มากกว่า 5 | 0<br>**3**<br>6 | `test_stars_out_of_range[0]`<br>`test_base_choice_is_saved`<br>`test_stars_out_of_range[6]` |
| **C2 Type of stars**<br>(ประเภทข้อมูลของดาว) | **จำนวนเต็ม / Integer (Base)**<br>ทศนิยม (Decimal)<br>ข้อความ (Text)<br>ไม่ส่งฟิลด์นี้ (Missing) | **3**<br>3.5<br>"3"<br>ไม่มีฟิลด์ stars | `test_base_choice_is_saved`<br>`test_stars_decimal`<br>`test_stars_text`<br>`test_stars_missing` |
| **C3 Pizza**<br>(การมีอยู่ของพิซซ่า) | **มีอยู่จริงในระบบ (Base)**<br>ไม่มีอยู่จริง | **พิซซ่าที่สร้างใหม่**<br>999999999 | `test_base_choice_is_saved`<br>`test_pizza_does_not_exist` |
| **C4 Token**<br>(ความถูกต้องของโทเคน) | **โทเคนของผู้ใช้เอง (Base)**<br>ไม่แนบโทเคน<br>โทเคนความยาวไม่ถูกต้อง | **จาก auth fixture**<br>ไม่มี Header<br>โทเคนสั้นเกินไป | `test_base_choice_is_saved`<br>`test_token_missing`<br>`test_token_wrong_length` |

---

## 4. โครงสร้างไฟล์ใน Repository (Repository Structure)

```text
api-lab/
├── .gitignore               # กำหนดไฟล์ที่ไม่ต้องนำเข้า Git
├── README.md                # เอกสารแนะนำโปรเจกต์และตาราง Input Domain Model (ภาษาไทย)
├── RESULTS.md               # ผลการทดลองและคำตอบแบบฝึกหัด Part 0, Defect Report, Part A, Part B (ภาษาไทย)
├── requirements.txt         # รายการแพ็กเกจที่ต้องติดตั้ง (pytest, requests, pytest-html)
├── report.html              # รายงานสรุปผลการรันชุดทดสอบรูปแบบ HTML
├── auth.txt                 # Header Authorization สำหรับทดสอบด้วย curl
├── veg.json                 # ข้อมูล Body สำหรับขอพิซซ่ามังสวิรัติด้วย curl
├── madeup.txt               # Header สำหรับทดสอบโทเคนปลอม 16 ตัวอักษร
├── conftest.py              # Pytest fixtures สำหรับจัดการ Session และข้อมูลทดสอบ
├── test_names.py            # Step 0.6: ทดสอบการแสดงรายชื่อพิซซ่า
├── test_tools.py            # Step 0.7: ทดสอบการแสดงรายการเครื่องมือด้วยโทเคน
├── test_pizza.py            # Step 0.8: ทดสอบการขอพิซซ่ามังสวิรัติและการปฏิเสธเมื่อไม่มีโทเคน
├── test_users.py            # Step 0.11: ทดสอบผู้ใช้ใหม่ที่เริ่มต้นโดยไม่มีเรตติ้ง
├── test_ratings.py          # Step 0.13-0.14: ทดสอบการทำงาน CRUD บนเรตติ้ง (สร้าง, อ่าน, แก้ไข, ลบ)
├── test_refused.py          # Step 0.15: ทดสอบการปฏิเสธคำขอ (ชื่อซ้ำ, รหัสผ่านผิด, ชื่อว่าง)
├── test_excluded_tools.py   # Step 0.16: ทดสอบการตัดเครื่องมือ และดักจับบั๊ก 500 (xfail)
├── test_create_rating.py    # Step A1-A2: ทดสอบสร้างเรตติ้งตามเกณฑ์ Base Choice Coverage (9 เคส)
├── test_update_rating.py    # Step A3: ทดสอบค่าขอบเขต (Boundary Values) ในการแก้ไขเรตติ้ง
└── test_rating_owner.py     # Step A4: ทดสอบการตรวจสอบสิทธิ์ความเป็นเจ้าของเรตติ้งข้ามผู้ใช้
```

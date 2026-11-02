# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: An Early Romana
- Step 0.12, results of the three runs without a session (optional): 
  - Run 1: 401 FAILED
  - Run 2: 200 PASSED
  - Run 3: 401 FAILED  
  *(เป็น Flaky test เกิดจากการไม่เก็บ Session Cookie ทำให้คำขอถูกกระจายไปยังเซิร์ฟเวอร์คนละเครื่องที่อยู่หลัง Load Balancer)*
- Step 0.16, blocks of "how many of the three tools are excluded":
  - Block 0 (ไม่ตัดเครื่องมือออกเลย / 0 ชิ้น): `[]`
  - Block 1 (ตัดเครื่องมือออก 1 ชิ้น): `["Knife"]`, `["Scissors"]`, `["Pizza cutter"]`
  - Block 2 (ตัดเครื่องมือออก 2 ชิ้น): `["Knife", "Scissors"]`, `["Knife", "Pizza cutter"]`, `["Pizza cutter", "Scissors"]`
  - Block 3 (ตัดเครื่องมือออกทั้ง 3 ชิ้น): `["Knife", "Pizza cutter", "Scissors"]`

## Defect report
- Title: เซิร์ฟเวอร์ตอบกลับด้วย 500 Internal Server Error (Body ว่าง) เมื่อลูกค้าตัดเครื่องมือออกทั้งหมด 3 ชิ้น
- Request: `POST /api/pizza` พร้อม Header `Authorization: token <token>` และ Body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: ควรได้รับสถานะ HTTP 400 Bad Request พร้อมข้อความแจ้งเตือนในรูปแบบ JSON ที่ชัดเจน (เช่น `{"error": "no pizza satisfies the excluded tools"}`) เนื่องจากไม่มีพิซซ่าใดตรงตามเงื่อนไข
- Actual result: ได้รับสถานะ HTTP 500 Internal Server Error โดยไม่มี Response Body (`Content-Length: 0`)
- Severity: ปานกลางถึงสูง (Medium to High) เนื่องจากเป็น Unhandled Server Exception (เซิร์ฟเวอร์แครช/เกิดข้อผิดพลาดที่ไม่ได้ดักจับ) ทำให้แอปพลิเคชันฝั่ง Client ไม่สามารถแสดงผลข้อความแจ้งเตือนที่ถูกต้องแก่ผู้ใช้งานได้

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - อ่าน (GET `/api/ratings/{id}`): ได้รับสถานะ `404 Not Found`
  - แก้ไข (PUT `/api/ratings/{id}`): ได้รับสถานะ `400 Bad Request`
  - ลบ (DELETE `/api/ratings/{id}`): ได้รับสถานะ `400 Bad Request`

## Part B
1. **ความล้มเหลว 2 ประเภทที่การทดสอบกับเซิร์ฟเวอร์จริงตรวจพบแต่ Unit Test ที่ใช้ Stubs ตรวจไม่พบ พร้อมเหตุผลที่ยังควรเขียน Unit Test:**
   - **สิ่งที่การทดสอบเซิร์ฟเวอร์จริงตรวจพบได้:**
     1. ปัญหาการทำงานร่วมกันระดับโครงสร้างพื้นฐาน (Integration & Environment Issues) เช่น การจัดการ HTTP Headers, การกำหนดเส้นทางของ Load Balancer ผ่านคุกกี้ Session (`AWSALB`), ปัญหา Network Latency และการตัดการเชื่อมต่อ
     2. ปัญหาข้อจำกัดของระบบจัดเก็บข้อมูลและ Schema ฝั่งเซิร์ฟเวอร์จริง (Database / Data Constraint Violations) เช่น การแปลงประเภทข้อมูลผิดพลาด (เช่น Go struct unmarshaling error เมื่อส่งประเภทข้อมูลที่ไม่ตรง), การจัดการ Race Condition, หรือปัญหาฐานข้อมูลจริง
   - **เหตุผลที่ยังต้องเขียน Unit Test with Stubs:**
     - ทำงานได้รวดเร็วมาก (ระดับมิลลิวินาที) และทำงานแบบแยกขาด (Isolation) โดยไม่ต้องพึ่งพาเซิร์ฟเวอร์ภายนอกหรือระบบเน็ตเวิร์ก ทำให้เมื่อเกิดข้อผิดพลาด สามารถชี้ชัดไปยังฟังก์ชันหรือตรรกะระดับโค้ดได้อย่างแม่นยำ

2. **เหตุผลที่ทุกการทดสอบต้องสร้าง User ใหม่แทนที่จะใช้ Public Token และการนำแนวคิดนี้ไปใช้ใน Project 2:**
   - ใน QuickPizza ข้อมูลถูกแชร์ร่วมกันกับผู้ทดสอบคนอื่นๆ หากใช้ Public Token ร่วมกัน เรตติ้งที่สร้างขึ้นอาจถูกเขียนทับ แก้ไข หรือลบโดยเทสต์อื่นหรือนักศึกษาคนอื่นที่รันพร้อมกัน (Test Interference) ส่งผลให้การทดสอบทำงานไม่เสถียร
   - **การประยุกต์ใช้ใน Project 2:** สำหรับระบบร้านค้า (Shop) หรือโรงแรม (Hotel) ที่แชร์ร่วมกัน แต่ละเทสต์ควรสร้างบัญชีผู้ใช้ชั่วคราว ข้อมูลสินค้า หรือหมายเลขการจองเฉพาะของตนเอง (Unique Test Identifiers) และทำการล้างข้อมูล (Teardown/Clean up) หลังจบเทสต์ เพื่อให้แต่ละเทสต์เป็นอิสระต่อกันโดยสมบูรณ์

3. **อธิบายเหตุผลที่ต้องส่ง Request ผ่าน Session เดียวกัน และผลลัพธ์จาก Step 0.12:**
   - QuickPizza ทำงานอยู่บนเซิร์ฟเวอร์หลายเครื่องหลัง AWS Application Load Balancer ซึ่งแต่ละเครื่องจะเก็บข้อมูลผู้ใช้แยกกัน เมื่อผู้ใช้ล็อกอิน Load Balancer จะส่งคุกกี้ชื่อ `AWSALB` กลับมา เพื่อระบุว่าคำขอถัดไปจากไคลเอนต์นี้จะต้องวิ่งไปยังเครื่องเดิม (Sticky Session) การใช้ `requests.Session()` จะช่วยเก็บและส่งคุกกี้นี้ไปพร้อมกับทุกคำขอโดยอัตโนมัติ
   - ใน Step 0.12 ที่ไม่ใช้ Session ผลลัพธ์จากการรัน 3 ครั้งพบว่า: ครั้งที่ 1 ไม่ผ่าน (ได้ 401), ครั้งที่ 2 ผ่าน (ได้ 200), และครั้งที่ 3 ไม่ผ่าน (ได้ 401) เนื่องจากคำขอล็อกอินถูก Load Balancer สุ่มส่งไปยังเซิร์ฟเวอร์เครื่องอื่นที่ไม่พบข้อมูลการสมัครสมาชิกของผู้ใช้ใหม่ จึงกลายเป็น **Flaky Test**

4. **Block ของ Excluded Tools ที่พบบั๊กใน Step 0.16, เหตุผลที่รหัส 500 แย่กว่า 400, และทำไมต้องใส่ xfail แทนที่จะลบทิ้ง:**
   - Block ที่พบบั๊กคือ Block ที่ 3: การตัดเครื่องมือออกทั้งหมด 3 ชิ้น (`["Knife", "Pizza cutter", "Scissors"]`)
   - รหัส **500 Internal Server Error** แย่กว่า 400 เพราะ 500 บ่งบอกว่าเกิดความล้มเหลวร้ายแรงที่ฝั่งเซิร์ฟเวอร์จนระบบหยุดทำงาน โดยไม่มีข้อความระบุสาเหตุที่นำไปจัดการต่อได้ ขณะที่ **400 Bad Request** แสดงว่าระบบทำงานปกติและสามารถระบุได้ว่าคำขอของฝั่งผู้ใช้ไม่ถูกต้อง ทำให้แอปพลิเคชันสามารถแจ้งข้อผิดพลาดให้ผู้ใช้เข้าใจและแก้ไขคำขอได้
   - การคงเทสต์ไว้ด้วย `@pytest.mark.xfail(strict=True)` ช่วยให้ทีมมองเห็นบั๊กที่ยังค้างอยู่เป็นรายงาน Known Issue โดยไม่ทำให้กระบวนการ CI/CD ทั้งหมดพัง และพารามิเตอร์ `strict=True` จะแจ้งเตือนทันทีที่ฝั่ง Backend แก้ไขบั๊กนี้สำเร็จ (เทสต์จะกลายเป็น Failed/XPASS) เพื่อเตือนให้เรานำแท็ก xfail ออก

5. **จำนวนการทดสอบของ Base Choice Coverage เทียบกับ All Combinations Coverage ใน Step A1:**
   - **Characteristics และ Blocks:**
     - C1 (Value of stars): 3 blocks
     - C2 (Type of stars): 4 blocks
     - C3 (Pizza): 2 blocks
     - C4 (Token): 3 blocks
   - **Base Choice Coverage (BCC):**
     $$1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9\text{ tests}$$
   - **All Combinations Coverage (ACC):**
     $$3 \times 4 \times 2 \times 3 = 72\text{ tests}$$

6. **Status Code ที่ได้ใน Step A4, สิ่งที่คาดหวัง และประเมินว่าเป็น Defect หรือไม่:**
   - Status Code ที่ได้รับจริง: การอ่าน (GET) ได้ `404 Not Found`, การแก้ไข (PUT) ได้ `400 Bad Request`, การลบ (DELETE) ได้ `400 Bad Request`
   - สิ่งที่คาดหวังตามมาตรฐาน REST และความปลอดภัย: ควรได้ `403 Forbidden` (เนื่องจากทรัพยากรมีอยู่จริง แต่ผู้ใช้ไม่มีสิทธิ์เข้าถึง) หรือ `404 Not Found` (หากระบบจงใจซ่อนทรัพยากรเพื่อไม่ให้คนอื่นเดา ID ได้)
   - การที่ PUT และ DELETE ตอบกลับด้วย `400 Bad Request` พร้อมข้อความว่า rating ID "not found" ถือเป็น **API Design Defect** ด้านความสอดคล้อง (Semantic Inconsistency) เนื่องจากรหัส 400 หมายถึงรูปแบบคำขอผิดพลาด (Malformed Request) ไม่ใช่ปัญหาเรื่องการหาทรัพยากรไม่พบหรือการละเมิดสิทธิ์

7. **ผลการทดสอบด้วย Token ปลอม (`0000000000000000`) จาก `madeup.txt` และความเสี่ยงบนระบบจริง:**
   - เมื่อรันคำสั่ง curl พบว่าเซิร์ฟเวอร์ตอบกลับด้วย **HTTP 200 OK** และส่งรายการเรตติ้งในระบบทั้งหมด 50 รายการกลับมา
   - นี่คือ **Defect ด้านความปลอดภัยที่ร้ายแรง (Broken Authentication / Improper Access Control)** เพราะเซิร์ฟเวอร์รับสตริงความยาว 16 ตัวอักษรใดๆ เป็น Token ที่ผ่านการอนุญาต โดยไม่ตรวจสอบว่าตรงกับเซสชันของผู้ใช้ที่มีอยู่จริงหรือไม่
   - บนระบบจริง คนแปลกหน้าหรือผู้โจมตีสามารถสุ่มสร้าง Token 16 ตัวอักษรเพื่อลักลอบดึงข้อมูลส่วนตัว (Data Scraping) ของผู้ใช้คนอื่น หรือสวมสิทธิ์เพื่อเข้าถึงทรัพยากรที่ไม่ได้รับอนุญาตได้

8. **สิ่งที่ API Test ตรวจสอบได้ดีกว่าการทดสอบผ่าน Web Page และสิ่งที่ทดสอบได้เฉพาะผ่าน Web Page เท่านั้น:**
   - **สิ่งที่ API Test ตรวจสอบได้ดีกว่า:** การทดสอบตรรกะทางธุรกิจฝั่งเซิร์ฟเวอร์ (Business Logic), โครงสร้างและประเภทข้อมูล Response (JSON Schema), ค่า Status Code, และการส่งข้อมูลขอบเขตสุดโต่ง/ข้อมูลที่ไม่ถูกต้อง (Negative / Malformed Inputs) ซึ่งหน้าเว็บมักจะบล็อกไว้ก่อนด้วย Client-side Validation
   - **สิ่งที่ทดสอบได้เฉพาะผ่าน Web Page:** การแสดงผลด้านภาพ (Visual Rendering), ความสวยงามของ CSS, ความลื่นไหลของ Animation, การจัดวางปุ่มและ Responsive Layout บนหน้าจอขนาดต่างๆ รวมถึงประสบการณ์การใช้งานจริงของผู้ใช้ (User Experience) และการเข้าถึง (Accessibility)

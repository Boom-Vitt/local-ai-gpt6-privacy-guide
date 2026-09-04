# GPT-6 Astra และ OpenAI Responses API

ตัวอย่างของ repository นี้อ้างอิง model ID ที่แน่นอนคือ [`gpt-6-astra`](https://developers.openai.com/api/docs/models/gpt-6-astra) ซึ่งรองรับ endpoint **Responses API** (`/v1/responses`). Model นี้กำลังทยอยเปิดให้ใช้; API project ของคุณอาจยังไม่มี access แม้ model ID จะปรากฏในเอกสาร. ให้ตรวจสิทธิ์ของ project และหน้า model ล่าสุดก่อนทำ integration.

ตัวอย่างที่ตรวจ payload แบบ offline อยู่ที่ [`../examples/openai_responses_masked.py`](../examples/openai_responses_masked.py). มันใช้ context สังเคราะห์ที่ mask แล้วและต้องเลือก `--send` อย่างชัดแจ้งก่อนมี network egress; repository นี้ไม่เรียก API จริงระหว่างการจัดทำคู่มือ.

## Payload และ API key

- ส่งเฉพาะข้อความบริบทขั้นต่ำที่ผ่าน masking และ pre-egress scan แล้ว; **ไม่ส่งไฟล์** ต้นฉบับ, raw text, local path, token map หรือ metadata ที่ไม่จำเป็น. ไม่ใช้ raw file upload เพื่อหลีกเลี่ยงขอบเขตนี้.
- ทุกตัวอย่างต้องส่ง `store=False`. ค่านี้ลด application-state storage ของ response สำหรับ request นั้น แต่ไม่ใช่คำรับประกันว่าไม่มีการเก็บข้อมูลทุกชนิด.
- อ่าน `OPENAI_API_KEY` จาก environment ของ process เท่านั้น ตาม [OpenAI quickstart](https://developers.openai.com/api/docs/quickstart); ห้ามวาง key ใน frontend, repository, prompt, telemetry หรือ log. Frontend ไม่ควรได้รับ key เลย.
- ผู้ใช้ต้องเห็น masked preview และอนุมัติก่อน egress ตาม [architecture](architecture.md) และ [privacy guidance](privacy-and-data-masking.md).

## `store=False` ไม่ใช่ Zero Data Retention

[Data controls ของ OpenAI](https://developers.openai.com/api/docs/guides/your-data) แยก **application-state storage** ออกจาก **abuse-monitoring logs**. สำหรับ Responses API, `store=False` ใช้ควบคุมการเก็บ application state ของ response; มันไม่ได้เปลี่ยน default abuse-monitoring logs ซึ่งอาจเก็บ customer content ได้นานสูงสุด 30 วัน. ดังนั้น `store=False` **ไม่ใช่** Zero Data Retention (ZDR) และไม่ควรใช้แทนการประเมิน data-retention requirement ขององค์กร.

ZDR และ Modified Abuse Monitoring (MAM) เป็น data controls สำหรับลูกค้าที่มีสิทธิ์ และต้องผ่านการอนุมัติจาก OpenAI พร้อมเงื่อนไขเพิ่มเติม. อย่ากล่าวอ้างว่า project มี ZDR/MAM จนกว่าจะยืนยัน eligibility และ approval ใน OpenAI settings/สัญญาขององค์กร. แม้ได้รับอนุมัติแล้ว ต้องอ่านข้อจำกัดตาม endpoint และ capability ในเอกสาร data controls ล่าสุด.

## Failure policy สำหรับ cloud egress

- ห้าม silent fallback จาก local model ไปยัง cloud; งาน hard ต้องผ่าน decision gate และ approval ใหม่
- ห้าม retry ด้วย raw data, raw file หรือ context ที่กว้างกว่าเดิม
- retry ได้แบบ bounded เฉพาะ masked payload ที่ผ่าน scan เดิมและยังอยู่ใน policy
- แสดง error แบบ redacted: ไม่พิมพ์ API key, raw prompt, file path, token map หรือ identifiers ลง log/error message

นโยบายนี้ช่วยลด egress ที่ไม่จำเป็น แต่ masking ไม่รับประกัน anonymization และไม่ได้แทน ZDR/MAM หรือข้อกำหนดด้านกฎหมายและนโยบายขององค์กร.

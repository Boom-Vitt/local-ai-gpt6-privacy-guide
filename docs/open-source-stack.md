# Open Source stack ที่ต้องตรวจ license แยกชั้น

เครื่องมือด้านล่างเป็น candidate สำหรับ workflow local-first ไม่ใช่รายการ dependency ที่ repository นี้ติดตั้งหรือรับรองว่าเหมาะกับทุกองค์กร. การประมวลผล local ลด API egress ได้ แต่ index, embeddings, token map และข้อมูลที่สร้างระหว่างทางยังอาจเป็นข้อมูลอ่อนไหวและต้องอยู่ภายใต้ access control กับ retention policy.

| Role | Candidate | License note |
| --- | --- | --- |
| Inference runtime | [vLLM](https://github.com/vllm-project/vllm) | Apache-2.0 code; hardware/model support varies. |
| PII orchestration | [Microsoft Presidio](https://github.com/microsoft/presidio) | MIT code; custom Thai recognizers required. |
| Thai NLP | [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) | Apache-2.0 library; inspect each model/data license. |
| OCR | [Tesseract](https://github.com/tesseract-ocr/tesseract) + Thai data | Apache-2.0; OCR errors can defeat masking. ตรวจ license ของ Thai traineddata ที่เลือกเพิ่มต่างหาก. |
| Local vectors | [Qdrant local mode](https://github.com/qdrant/qdrant) | Apache-2.0; index remains sensitive. |

## Runtime license is not model license

license ของ runtime หรือ library ไม่ได้อนุญาต model weights, tokenizer, model card, dataset หรือ output terms โดยอัตโนมัติ. ก่อนดาวน์โหลดหรือใช้ model ใด โดยเฉพาะในงานเชิงพาณิชย์ ให้ review เอกสารและเงื่อนไขของผู้เผยแพร่สำหรับ:

- **model-card** และ intended use / known limitations
- สิทธิ์ **commercial-use** และเขตอำนาจหรือข้อจำกัดตามองค์กร
- ข้อกำหนด **attribution** หรือ notice ที่ต้องแสดง
- สิทธิ์และข้อห้ามเรื่อง **redistribution** ของ weights, tokenizer และไฟล์ประกอบ
- เงื่อนไขของ **derivative-work**, fine-tune, adapter และการเผยแพร่ผลลัพธ์
- license ของ training data, benchmark, Thai model/data และไฟล์เสริมที่แยกจาก code

จึงไม่มี model เดียวที่ปลอดภัยหรือใช้ได้อย่างสากลสำหรับทุก use case. ให้ยืนยัน license และ policy ตามรุ่น, revision, source และวัตถุประสงค์ที่จะนำไปใช้จริง และเก็บผลการ review ไว้กับการอนุมัติ deployment.

## ขอบเขตข้อมูล local

แม้เลือก component ที่เป็น Open Source แล้ว ข้อมูลที่ผ่าน OCR, chunks, embeddings, local vector index และ token map ยังเป็นข้อมูล **sensitive**. แนวทางใน [architecture](architecture.md) และ [privacy and data masking](privacy-and-data-masking.md) ให้เก็บสิ่งเหล่านี้ในเครื่อง, จำกัดสิทธิ์, กำหนด retention และไม่ส่ง token map หรือ raw context ออกผ่าน API.

# เลือกเส้นทาง Local AI ตามแพลตฟอร์ม

หน้านี้เป็นแผนที่สำหรับตรวจความพร้อมก่อนเลือก runtime local ไม่ใช่คู่มือติดตั้ง และ repository นี้ **ไม่ติดตั้ง** vLLM, `vllm-metal`, driver, Python package หรือ model weights ให้บนเครื่องใด ๆ. ห้ามสรุปจากตารางนี้ว่า `pip install vllm` คำสั่งเดียวจะใช้ได้กับทุกระบบหรือทุก hardware.

## Platform matrix

| ระบบ | เส้นทางที่อธิบาย | ข้อจำกัดและสิ่งที่ต้องตรวจ |
| --- | --- | --- |
| Linux | เป็นเส้นทาง vLLM ที่มีเอกสารหลัก: ดู [GPU installation](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/) และ [CPU installation](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/) แล้วเลือกเส้นทาง CUDA, ROCm, XPU หรือ CPU ที่ตรงกับเครื่อง | Linux เป็นฐานของเอกสาร GPU หลัก แต่ CUDA/ROCm/XPU และ CPU มีข้อกำหนดต่างกัน; ต้องตรวจรุ่น hardware, driver, Python และ model ที่รองรับก่อนติดตั้ง ไม่รับประกันว่า accelerator ทุกตัวใช้ได้. |
| Windows | vLLM **ไม่รองรับ native Windows**; ใช้ Linux distribution ภายใต้ **WSL2** เมื่อ hardware และ driver รองรับ และอ้างอิง [CUDA on WSL ของ Microsoft](https://learn.microsoft.com/windows/ai/directml/gpu-cuda-in-wsl) | community forks ไม่ใช่ official support ของ vLLM. ตรวจความเข้ากันได้ของ Windows, WSL2, NVIDIA driver/CUDA และ Linux guest เอง; อย่าถือว่า binary หรือคำสั่งจาก Linux จะทำงานบน Windows host โดยตรง. |
| macOS Apple Silicon | เส้นทาง vLLM CPU บน Apple Silicon เป็น **experimental** และต้อง build from source ตาม [CPU installation](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/). สำหรับ GPU acceleration มี [vllm-metal](https://github.com/vllm-project/vllm-metal), community hardware plugin ที่ใช้ MLX/Metal | ไม่ใช่เส้นทางที่เทียบเท่า Linux-CUDA. `vllm-metal` เป็น community project; ต้องตรวจ macOS, Xcode/Command Line Tools, Python, รุ่นชิป และ model support ตามเอกสารของมันก่อนตัดสินใจใช้. |

## Hardware checklist ก่อนเลือก runtime

ตรวจรายการต่อไปนี้กับเอกสารของ runtime และ model ที่จะใช้จริง ไม่อนุมานจากชื่อ GPU หรือขนาด model เพียงอย่างเดียว:

- **Architecture:** CPU/GPU architecture และ instruction set ที่ runtime รองรับ
- **RAM/VRAM:** หน่วยความจำสำหรับ weights, KV cache, concurrent requests และ overhead ของระบบ
- **Storage:** พื้นที่สำหรับ weights, cache, build artifacts และดัชนี local ที่อาจมีข้อมูลอ่อนไหว
- **Driver:** รุ่น OS, GPU driver, CUDA/ROCm/XPU stack หรือ Metal ที่ตรงกับเส้นทางนั้น
- **Python:** รุ่น Python และ toolchain ที่เอกสารของ runtime ระบุ
- **Context length:** ขนาด context/KV cache ที่ workload ต้องใช้ ไม่ใช่แค่ context สูงสุดบน model card
- **Model format:** architecture, precision/quantization และ format ของ weights ที่ runtime รองรับ
- **License:** license ของ runtime, model weights, training data และเงื่อนไขการใช้งานเชิงพาณิชย์แยกกัน

## ขอบเขตของ repository นี้

คู่มือนี้อธิบายทางเลือกและข้อควรตรวจเท่านั้น: ไม่ติดตั้งซอฟต์แวร์, ไม่ดาวน์โหลด model, ไม่รัน local model และไม่เปลี่ยนการตั้งค่าของเครื่องผู้อ่าน. เมื่อเลือกเส้นทางได้แล้ว ให้ทำตามเอกสารต้นทางของแต่ละ platform ใน environment ที่แยกและตรวจสอบได้.

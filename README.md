# 🎧 Anki Connect Edge TTS - Tự động tạo Audio cho Anki

Ứng dụng mạnh mẽ, đơn giản và tối ưu nhất để tạo âm thanh (Text-to-Speech) cho thẻ bài Anki bằng công nghệ Microsoft Edge TTS. Bản cập nhật đặc biệt dành cho sinh viên Y khoa và người học ngoại ngữ.

> **Made with ❤️ by PonZ**

---

## 🌟 Ý tưởng & Cảm hứng

Dự án này được ra đời từ nhu cầu thực tế trong việc học tập khối lượng kiến thức khổng lồ của ngành Y. Việc nghe âm thanh giúp ghi nhớ tốt hơn, nhưng các công cụ hiện có thường phức tạp hoặc đọc không tự nhiên.

**Cảm hứng:** Dự án được lấy cảm hứng và kế thừa ý tưởng từ [msjsc001/Anki-TTS-Edge](https://github.com/msjsc001/Anki-TTS-Edge). Tôi đã phát triển lại với giao diện Streamlit hiện đại, thêm các bộ lọc thông minh dành riêng cho thuật ngữ Y khoa và khả năng quản lý Deck trực quan hơn.

---

## ✨ Tính năng nổi bật

- **🚀 Quét & Quản lý Thông minh**:
  - **Scan Status**: Biết ngay Deck/Tag nào còn thiếu audio.
  - **Smart Fill**: Chỉ tạo audio cho những thẻ còn trống (tiết kiệm thời gian).
  - **Clear Audio**: Xóa sạch audio cũ trong một nốt nhạc để làm lại từ đầu.
- **🩺 Tối ưu ngành Y**:
  - Tự động giải mã từ viết tắt (VD: `BN` -> `Bệnh nhân`, `THA` -> `Tăng huyết áp`).
  - Lọc sạch rác văn bản: Emojis, số tham khảo `[1]`, các ký tự ẩn phá vỡ âm thanh.
- **🗣️ Công nghệ âm thanh cao cấp**:
  - **SSML Advanced**: Dùng giọng Nam đọc câu hỏi, giọng Nữ trả lời, ngắt nghỉ 1 giây chuyên nghiệp.
  - **Simple Mode**: Chế độ "chống điếc" - cực kỳ ổn định, không bao giờ đọc nhầm mã nguồn.
  - **Speed Control**: Chỉnh tốc độ từ 0.5x đến 1.5x (mặc định 0.9x cho dễ nghe).
- **🎨 Giao diện Streamlit**: Sử dụng trực tiếp trên trình duyệt, trực quan và dễ dùng.

---

## 🛠️ Hướng dẫn cài đặt chi tiết

### 1. Yêu cầu hệ thống

- Đã cài đặt **Python 3.9+**
- Phần mềm **Anki** đang mở trên máy tính.

### 2. Cài đặt AnkiConnect (Bắt buộc)

App này giao tiếp với Anki qua plugin **AnkiConnect**.

1. Mở Anki -> **Tools** -> **Add-ons**.
2. Chọn **Get Add-ons**, nhập mã: `2055492159`.
3. Sau khi cài xong, chọn AnkiConnect -> **Config** và dán đoạn này vào:

   ```json
   {
       "apiKey": null,
       "apiLogPath": null,
       "ignoreOriginList": [],
       "webBindAddress": "127.0.0.1",
       "webBindPort": 8765,
       "webCorsOriginList": ["*"]
   }
   ```

4. **Khởi động lại Anki**.

### 3. Cài đặt App

1. Tải source code về máy.
2. Mở Terminal (Command Prompt) tại thư mục dự án và chạy các lệnh sau:

   ```bash
   # Tạo môi trường ảo (khuyên dùng)
   python -m venv .venv

   # Kích hoạt môi trường ảo
   # Trên Mac/Linux:
   source .venv/bin/activate
   # Trên Windows:
   .venv\Scripts\activate

   # Cài đặt các thư viện cần thiết
   pip install -r requirements.txt
   ```

---

## 🚀 Cách sử dụng

1. **Chạy App:**

    ```bash
    streamlit run streamlit_app.py
    ```

2. **Cấu hình trên giao diện:**
    - Chọn **Deck** và **Tag** của thẻ bài cần tạo tiếng.
    - Nhập tên trường chứa văn bản (VD: `Front, Back`) và trường sẽ lưu Audio (VD: `Audio`).
    - Chọn giọng đọc (Khuyên dùng `NamMinh` hoặc `HoaiMy` cho tiếng Việt).
3. **Kiểm tra:** Bấm **Preview Random Note** để nghe thử một thẻ bất kỳ.
4. **Thực thi:** Bấm **Start Batch Generation** và ngồi uống cafe chờ máy làm việc!

---

## 📝 Bản quyền (Copyright)

Dự án được phát hành dưới giấy phép **LGPL-3.0**.

- Phần lõi Edge-TTS thuộc về các tác giả gốc.
- Phần giao diện và logic quản lý Anki được phát triển bởi **PonZ**.

**Copyright (c) 2026 PonZ.**
Tất cả các đóng góp hoặc sao chép vui lòng giữ lại nguồn và tên tác giả.

---
*Chúc anh/chị học tập thật tốt với những chiếc thẻ bài "vibe" nhất!* 🎧📖

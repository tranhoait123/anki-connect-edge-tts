# 🎧 Anki Connect Edge TTS - Tự động tạo Audio cho Anki

Ứng dụng mạnh mẽ, đơn giản và tối ưu nhất để tạo âm thanh (Text-to-Speech) cho thẻ bài Anki bằng công nghệ Microsoft Edge TTS. Bản cập nhật đặc biệt dành cho sinh viên Y khoa và người học ngoại ngữ.

> **Made with ❤️ by PonZ**
>
> [English Version (README_EN.md)](./README_EN.md)

---

## 🌟 Ý tưởng & Cảm hứng

Dự án này được ra đời từ nhu cầu thực tế trong việc học tập khối lượng kiến thức khổng lồ của ngành Y. Việc nghe âm thanh giúp ghi nhớ tốt hơn, nhưng các công cụ hiện có thường phức tạp hoặc đọc không tự nhiên.

**Cảm hứng:** Dự án được lấy cảm hứng và kế thừa ý tưởng từ [msjsc001/Anki-TTS-Edge](https://github.com/msjsc001/Anki-TTS-Edge). Tôi đã phát triển lại với giao diện Streamlit hiện đại, thêm các bộ lọc thông minh dành riêng cho thuật ngữ Y khoa và khả năng quản lý Deck trực quan hơn.

---

## ✨ Tính năng nổi bật

- **🚀 Quét & Quản lý Thông minh**:
  - **Scan Status**: Biết ngay Deck/Tag nào còn thiếu audio. Trả về báo cáo tổng số thẻ, thẻ đã có và thẻ chưa có audio.
  - **Smart Fill**: Chỉ tạo audio cho những thẻ còn trống (tiết kiệm thời gian, tránh trùng lặp).
  - **Clear Audio**: Xóa sạch audio cũ trong trường dữ liệu để làm lại từ đầu.
- **🩺 Tối ưu ngành Y & Ngôn ngữ**:
  - **Abbreviation Expansion**: Tự động giải mã từ viết tắt (VD: `BN` -> `Bệnh nhân`, `THA` -> `Tăng huyết áp`). Bạn có thể tùy chỉnh danh sách từ viết tắt ngay trên giao diện.
  - **Text Cleaning**: Tự động loại bỏ rác văn bản: Emojis, số tham khảo `[1]`, các ký tự ẩn phá vỡ âm thanh, mã HTML, v.v.
- **🗣️ Công nghệ âm thanh cao cấp**:
  - **SSML Advanced**: Dùng giọng Nam đọc câu hỏi, giọng Nữ trả lời, ngắt nghỉ 1 giây chuyên nghiệp giữa các trường.
  - **Simple Mode (Chống lỗi đọc mã)**: Chế độ gửi văn bản thuần túy cho máy chủ Microsoft. Đảm bảo cực kỳ ổn định, không bao giờ xảy ra lỗi đọc nhầm mã nguồn XML.
  - **Speed Control**: Chỉnh tốc độ từ 0.5x đến 1.5x (mặc định 0.9x cho dễ nghe nội dung chuyên môn).
- **🎨 Giao diện Streamlit**: Hoạt động trực tiếp trên trình duyệt, trực quan, hỗ trợ tự động lưu mọi cài đặt cho lần sử dụng sau.

---

## 🛠️ Hướng dẫn cài đặt chi tiết

### 1. Yêu cầu hệ thống

- Máy tính đã cài đặt **Python 3.9** trở lên.
- Phần mềm **Anki** phải đang mở khi sử dụng ứng dụng.

### 2. Cài đặt AnkiConnect (Bắt buộc)

App này giao tiếp với Anki qua plugin **AnkiConnect**.

1. Mở Anki -> **Tools** -> **Add-ons**.
2. Chọn **Get Add-ons**, nhập mã: `2055492159`.
3. Sau khi cài xong, chọn AnkiConnect trong danh sách -> chọn **Config**.
4. Dán chính xác đoạn cấu hình sau vào ô bên phải để cho phép App truy cập:

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

5. **Khởi động lại Anki** để lưu thay đổi.

### 3. Cài đặt App trên máy tính

1. Tải toàn bộ mã nguồn về máy tính.
2. Mở Terminal (Command Prompt) tại thư mục dự án và chạy các lệnh:

   ```bash
   # Tạo môi trường ảo (Khuyên dùng để tránh xung đột thư viện)
   python -m venv .venv

   # Kích hoạt môi trường ảo
   # Trên Windows:
   .venv\Scripts\activate
   # Trên Mac/Linux:
   source .venv/bin/activate

   # Cài đặt các thư viện cần thiết
   pip install -r requirements.txt
   ```

---

## 🚀 Cách sử dụng

1. **Chạy App:** Trong cửa sổ Terminal đang kích hoạt môi trường ảo, gõ:

    ```bash
    streamlit run streamlit_app.py
    ```

2. **Cấu hình trên giao diện:**
    - **Deck/Tag**: Chọn nhóm thẻ bài bạn muốn thêm audio.
    - **Fields**: Nhập tên trường chứa văn bản (VD: `Front, Back`) và tên trường lưu Audio (VD: `Audio`). Lưu ý: Tên trường phải trùng khớp chính xác 100% với tên trường trong Anki của bạn.
    - **Voice**: Chọn ngôn ngữ và giọng đọc phù hợp.
3. **Xem trước (Preview):** Luôn bấm **Preview Random Note** để nghe thử tốc độ và chất lượng trước khi chạy hàng loạt.
4. **Thực thi:** Bấm **Start Batch Generation**. App sẽ hiển thị tiến độ và nội dung đang xử lý trực tiếp trên màn hình.

---

## 🔍 Giải thích kỹ thuật & Khắc phục lỗi

### SSML vs Simple Mode

- **SSML (Advanced)**: Sử dụng mã XML để điều khiển giọng đọc (ngắt nghỉ, đa giọng). Phức tạp nhưng giọng đọc sẽ chuyên nghiệp hơn.
- **Simple Mode**: Chế độ an toàn, chỉ gửi chữ thuần. Hãy bật chế độ này nếu bạn thấy máy bắt đầu đọc mớ mã lệnh như `speak version 1.0`.

### Các lỗi thường gặp

1. **"Could not connect to Anki"**: Hãy kiểm tra xem Anki đã mở chưa và bạn đã cài đúng cấu hình AnkiConnect trong bước 2 chưa.
2. **"Field not found"**: Kiểm tra lại tên trường trong Anki (Phân biệt chữ hoa/chữ thường). Ví dụ `front` khác với `Front`.
3. **Lỗi máy đọc mã lệnh**: Bật **Simple Mode** trên giao diện App.

---

## 📝 Bản quyền & Đóng góp

Dự án được phát hành dưới giấy phép **LGPL-3.0**.

- Phần lõi Edge-TTS thuộc về các tác giả gốc (Christopher Down & Rany).
- Toàn bộ logic giao diện, lọc văn bản Y khoa và quản lý Anki được phát triển bởi **PonZ**.

**Copyright (c) 2026 PonZ.**

---
*Mọi ý kiến đóng góp hoặc báo lỗi vui lòng liên hệ qua hệ thống GitHub Issue của dự án. Chúc bạn học tập hiệu quả!* 🎧📖

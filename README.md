# 🎧 Anki Connect Edge TTS - Giải Pháp Tự Động Hóa Audio Toàn Diện cho Anki

Chào mừng bạn đến với công cụ tối ưu nhất để nâng tầm trải nghiệm học tập trên Anki. Đây không chỉ là một trình tạo âm thanh thông thường, mà là một hệ thống được thiết kế tỉ mỉ để giúp bạn học tập "nhanh hơn, nhớ lâu hơn" thông qua sức mạnh của âm thanh.

> **Made with ❤️ by PonZ**
>
> [English Version Available (README_EN.md)](./README_EN.md)

---

## 📖 Mục đích dự án

Việc học thẻ bài (flashcards) chỉ với văn bản thường gây nhàm chán và khó ghi nhớ phát âm, đặc biệt là với các thuật ngữ Y khoa phức tạp hoặc ngôn ngữ mới. Dự án này được tạo ra để:

1. **Tiết kiệm thời gian**: Thay vì ngồi tạo từng file audio thủ công, bạn có thể tạo hàng nghìn file chỉ trong vài phút.
2. **Tăng cường trí nhớ**: Sự kết hợp giữa mắt nhìn và tai nghe kích thích não bộ ghi nhớ sâu hơn.
3. **Tối ưu hóa quy trình**: Quản lý Deck chuyên nghiệp, bù đắp audio thiếu hụt mà không làm xáo trộn dữ liệu cũ.

**Cảm hứng:** Được kế thừa và phát triển từ ý tưởng gốc của [msjsc001/Anki-TTS-Edge](https://github.com/msjsc001/Anki-TTS-Edge), tôi đã tái cấu trúc hoàn toàn giao diện và logic để phù hợp hơn với người dùng Việt Nam, đặc biệt là cộng đồng sinh viên Y khoa.

---

## ✨ Tính năng chi tiết (Mọi thứ bạn cần)

### 1. 🚀 Quản lý Deck Thông minh

- **🔍 Scan Status (Quét tình trạng)**: Bạn có hàng nghìn thẻ bài và không biết thẻ nào có tiếng, thẻ nào chưa? Chỉ cần 1 click, App sẽ báo cáo:
  - Tổng số thẻ hiện có.
  - Số thẻ đã có sẵn âm thanh.
  - Số thẻ đang bị "câm" (thiếu audio).
- **⚡ Smart Fill (Chạy bù)**: App đủ thông minh để nhận diện những thẻ đã có tiếng và bỏ qua chúng, chỉ tập trung xử lý những thẻ còn thiếu. Điều này cực kỳ hữu ích khi bạn thêm thẻ mới vào một bộ Deck lớn.
- **🗑️ Clear Audio (Làm sạch)**: Muốn thay đổi giọng đọc cho toàn bộ Deck? Nút xóa sẽ giúp bạn làm sạch trường Audio để sẵn sàng cho một đợt tạo mới.

### 2. 🩺 Tối ưu hóa cho Chuyên ngành & Ngôn ngữ

- **📝 Abbreviation Expansion (Giải mã từ viết tắt)**: Tính năng "vàng" cho sinh viên Y khoa.
  - Ví dụ: Bạn nhập `BN=Bệnh nhân`, khi máy gặp chữ `BN` nó sẽ đọc đầy đủ là "Bệnh nhân".
  - Hỗ trợ danh sách tùy chỉnh không giới hạn ngay trên giao diện.
- **🧹 Text Cleaning Pro (Dọn dẹp văn bản)**:
  - Loại bỏ icon, emoji, các ký tự lạ.
  - Xóa bỏ các số tham khảo nhỏ trong bài viết (VD: `[1]`, `[2,3]`).
  - Loại bỏ mã HTML thừa để máy không đọc nhầm.

### 3. 🎙️ Công nghệ Audio Đỉnh cao (Edge TTS)

- **🎭 SSML Advanced (Đa giọng đọc)**: Cho phép cấu hình giọng Nam đọc Câu hỏi và giọng Nữ đọc Câu trả lời (hoặc ngược lại) để tạo sự phân biệt rõ ràng khi học. Có thêm đoạn nghỉ 1 giây để não bộ kịp xử lý.
- **🛡️ Simple Mode (Chế độ an toàn)**: Nếu bạn gặp tình trạng máy đọc luôn cả mã lệnh (XML), hãy bật chế độ này. App sẽ gửi văn bản thuần túy, đảm bảo 100% không lỗi.
- **🐢 Speed Control (Tốc độ)**: Tùy chỉnh từ đọc chậm (để nghe rõ phát âm) đến đọc nhanh (để ôn tập). Khuyên dùng **0.9x** cho kiến thức chuyên môn.

---

## 🛠️ Hướng dẫn cài đặt "Cầm tay chỉ việc"

### Bước 1: Chuẩn bị môi trường (Làm 1 lần duy nhất)

1. Tải và cài đặt **Python** từ [python.org](https://www.python.org/downloads/). (Lưu ý tích chọn **"Add Python to PATH"** khi cài đặt).
2. Tải mã nguồn này về máy và giải nén.

### Bước 2: Thiết lập Anki & AnkiConnect

Dự án cần "quyền" để nói chuyện với Anki của bạn.

1. Mở phần mềm Anki trên máy tính.
2. Vào **Tools** -> **Add-ons** -> **Get Add-ons**.
3. Nhập mã: `2055492159` để cài **AnkiConnect**.
4. Sau khi cài, chọn AnkiConnect -> **Config** và dán đoạn này vào:

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

5. **Quan trọng**: Tắt Anki và mở lại.

### Bước 3: Cài đặt thư viện hỗ trợ

1. Mở thư mục code vừa tải về.
2. Nhấp chuột phải vào vùng trống, chọn **Open in Terminal** (hoặc Command Prompt).
3. Chạy lệnh để tạo môi trường sạch:

    ```bash
    python -m venv .venv
    ```

4. Kích hoạt nó:
    - **Windows**: `.venv\Scripts\activate`
    - **Mac/Linux**: `source .venv/bin/activate`
5. Cài đặt các gói cần thiết:

    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Hướng dẫn sử dụng thực tế

1. **Khởi động**: Tại Terminal, gõ `streamlit run streamlit_app.py`. Một trang web sẽ hiện ra.
2. **Kết nối**: App sẽ hiện "Connected to Anki" màu xanh ở bên trái. Nếu hiện màu đỏ, hãy kiểm tra xem Anki của bạn đã mở chưa.
3. **Lọc dữ liệu**:
    - Chọn **Deck** (Bộ thẻ).
    - Nhập **Tag** (Nhãn) nếu bạn chỉ muốn tạo tiếng cho một phần của Deck.
4. **Cấu hình Trường (Fields)**:
    - **Source Fields**: Tên các ô chứa chữ (VD: `Front, Back`). Chữ trong các ô này sẽ được đọc lên.
    - **Target Field**: Tên ô sẽ chứa file âm thanh (VD: `Audio`).
5. **Chọn Giọng**: Chọn Ngôn ngữ là `vi-VN` và chọn giọng `NamMinh` (Trầm ấm) hoặc `HoaiMy` (Nhẹ nhàng).
6. **Thực hiện**: Bấm **Start Batch Generation** và theo dõi thanh tiến trình.

---

## 🔍 Giải đáp thắc mắc (FAQ) & Sửa lỗi

- **Hỏi: Tại sao App báo không kết nối được với Anki?**
  - *Đáp*: Hãy chắc chắn Anki đang mở và bạn đã làm đúng Bước 2 phần Cấu hình AnkiConnect.
- **Hỏi: Máy đọc luôn cả mấy chữ "speak version 1.0", xử lý sao?**
  - *Đáp*: Đây là lỗi nhận diện SSML của Microsoft. Hãy tích chọn **Simple Mode** trên App, lỗi này sẽ biến mất hoàn toàn.
- **Hỏi: Tôi muốn sửa lại file Audio vì tốc độ hơi nhanh?**
  - *Đáp*: Chỉnh lại tốc độ, tích chọn **"Force overwrite existing audio"** và chạy lại. App sẽ ghi đè file mới lên.

---

## 📝 Giấy phép & Bản quyền

Dự án sử dụng giấy phép **LGPL-3.0**.

- Mọi thành quả của bạn tạo ra (audio) là của bạn.
- Vui lòng giữ lại ghi chú **Made by PonZ** nếu bạn chia sẻ hoặc phát triển lại công cụ này.

**Copyright (c) 2026 PonZ.**

---
*Hy vọng công cụ này sẽ giúp hành trình chinh phục kiến thức của bạn trở nên thú vị và nhẹ nhàng hơn!* 🎧📚

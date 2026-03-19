import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
# Headers giả lập chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
}
    print("=" * 60)
    print("     CHƯƠNG TRÌNH TRA CỨU BÁO CÁO TÀI CHÍNH CAFEF.VN")
    print("=" * 60)

    while True:
        #Input mã cổ phiếu
        stock_code = input("Nhập mã cổ phiếu (VD: VCB, TCB, FPT, ACB) [hoặc 'Quit' để thoát]: ").strip().upper()
        
        if stock_code.lower() == 'quit' or stock_code.lower() == 'exit' or stock_code.lower() == 'q' or stock_code.lower() == 'e':
            print("Đang thoát chương trình. Hẹn gặp lại!\n")
            break
        
        if not stock_code:
            print("Vui lòng nhập mã cổ phiếu hợp lệ.")
            continue
        
        #Input sàn chứng khoán
        print("Chọn sàn giao dịch:")
        print("     1. HOSE (Sở GDCK TP.HCM)")
        print("     2. HNX (Sở GDCK Hà Nội)")
        print("     3. UPCOM")
        exchange_choice = input("Nhập lựa chọn: ").strip()
        
        #Define sàn chứng khoán
        if exchange_choice == '1':
            exchange = 'hose'
            exchange_name = 'HOSE'
        elif exchange_choice == '2':
            exchange = 'hnx'
            exchange_name = 'HNX'
        elif exchange_choice == '3':
            exchange = 'upcom'
            exchange_name = 'UPCOM'
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, hoặc 3.")
            continue
        
        
        # Tạo URL
        url = f"https://cafef.vn/du-lieu/{exchange}/{stock_code.lower()}-bao-cao-tai-chinh.chn"
        
        print("\n" + "=" * 60)
        print(f" ĐANG KIỂM TRA: Mã {stock_code} - Sàn {exchange_name}")
        print(f" URL: {url}")
        print("=" * 60)

        
        try:
            # Gửi request GET 
            response = requests.get(url, headers=headers, timeout=15)
    
            # Kiểm tra status code
            print(f"Status Code: {response.status_code}")
    
            if response.status_code == 200:
                print("Kết nối thành công!")
        
                # Phân tích HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Lấy tiêu đề trang
                title = soup.find('title')
                if title:
                    print(f"Tiêu đề: {title.get_text().strip()}")
                
                # Đếm số lượng
                links = soup.find_all('a')
                tables = soup.find_all('table')
                print(f"Tổng số link: {len(links)}")
                print(f"Số bảng: {len(tables)}")
                
                # Tìm link PDF
                pdf_links = soup.find_all('a', href=lambda href: href and href.lower().endswith('.pdf'))
                print(f"Số file PDF: {len(pdf_links)}")
                
                pdf_list = []
                
                if pdf_links:
                    print("\n" + "=" * 60)
                    print("📋 DANH SÁCH TẤT CẢ FILE PDF")
                    print("=" * 60)
                    
                    for i, link in enumerate(pdf_links, start=1):
                        #Lấy tên file PDF
                        report_name = link.get_text(strip=True)
                        #Nếu tên file PDF trống, thử lấy từ thẻ cha
                        if not report_name:
                            parent = link.find_parent('td')
                            if parent:
                                report_name = parent.get_text(strip=True)
                            else:
                                report_name = "Không có tên"
                        
                        # Lấy href và tạo URL đầy đủ
                        href = link.get('href')
                        full_url = urljoin(url, href)  # Chuyển link tương đối thành tuyệt đối

                        # Lưu vào list
                        pdf_info = {
                            'stt': i,
                            'ten_bao_cao': report_name,
                            'link': full_url
                        }
                        pdf_list.append(pdf_info)
                        
                        # In ra màn hình
                        print(f"\n📄 PDF #{i}:")
                        print(f"   📌 Tên: {report_name}")
                        print(f"   📎 Link: {full_url}")
                        
                        # Thêm dấu phân cách sau mỗi 5 file để dễ đọc
                        if i % 5 == 0 and i < len(pdf_links):
                            print("-" * 40)
                
            elif response.status_code == 404:
                print(f"ERROR: KHÔNG TÌM THẤY: Mã {stock_code} không tồn tại trên sàn {exchange_name}")
                print("--> Thử kiểm tra trên sàn khác hoặc kiểm tra lại mã cổ phiếu")
            elif response.status_code == 403:
                print("ERROR: BỊ CHẶN: Server từ chối truy cập")
                print("--> Thử thay đổi User-Agent hoặc dùng proxy")
            else:
                print(f"ERROR: LỖI: Status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("ERROR: LỖI KẾT NỐI: Không thể kết nối đến server")
        except requests.exceptions.Timeout:
            print("ERROR: LỖI TIMEOUT: Quá thời gian chờ")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: LỖI REQUEST: {e}")
        except Exception as e:
            print(f"ERROR: LỖI KHÔNG XÁC ĐỊNH: {e}")
        
        print("\n" + "-" * 40)
        input("Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()

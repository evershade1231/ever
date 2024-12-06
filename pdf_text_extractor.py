from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path, page_number):
    try:
        # PDF 파일 읽기
        reader = PdfReader(file_path)
        
        # 지정된 페이지의 텍스트 추출
        if page_number <= len(reader.pages):
            return reader.pages[page_number - 1].extract_text()
        else:
            return "해당 페이지가 없습니다."
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 테스트 실행
if __name__ == "__main__":
    file_path = input("PDF 파일 경로를 입력하세요: ")
    page_number = int(input("확인할 페이지 번호를 입력하세요: "))
    
    result = extract_text_from_pdf(file_path, page_number)
    print("\n추출된 텍스트:")
    print(result)

from PyPDF2 import PdfReader
import requests

# PDF에서 텍스트 추출 함수
def extract_text_from_pdf(file_path, page_number):
    try:
        reader = PdfReader(file_path)
        if page_number <= len(reader.pages):
            return reader.pages[page_number - 1].extract_text()
        else:
            return "해당 페이지가 없습니다."
    except Exception as e:
        return f"오류 발생: {str(e)}"

# Google Cloud Translation API 번역 함수
def translate_text(text, target_language="ko"):
    api_key = "AIzaSyCk7EoNf3sVvEkOoB6ChghxJ2q2URQnW90"  # API 키 입력
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "key": api_key
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = response.json()
        return result["data"]["translations"][0]["translatedText"]
    else:
        return f"번역 오류: {response.status_code} - {response.text}"

# 프로그램 실행
if __name__ == "__main__":
    file_path = input("PDF 파일 경로를 입력하세요: ")
    page_number = int(input("번역할 페이지 번호를 입력하세요: "))

    # PDF에서 텍스트 추출
    text = extract_text_from_pdf(file_path, page_number)
    print("\n추출된 텍스트:")
    print(text)

    # 추출된 텍스트 번역
    if text and text != "해당 페이지가 없습니다.":
        translated = translate_text(text)
        print("\n번역된 텍스트:")
        print(translated)
    else:
        print("\n텍스트를 추출할 수 없습니다.")

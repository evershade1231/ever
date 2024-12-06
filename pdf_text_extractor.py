import os
import streamlit as st
from PyPDF2 import PdfReader
from google.cloud import translate_v2 as translate

# Google Translate API 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Google Translate API 클라이언트 초기화
def translate_text(text, target_language="ko"):
    try:
        client = translate.Client()
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        st.error(f"번역 중 오류 발생: {e}")
        return None

# PDF 파일에서 텍스트 추출 함수
def extract_text_from_pdf(file, page_number):
    try:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        if page_number > num_pages or page_number < 1:
            st.error(f"유효하지 않은 페이지 번호입니다. PDF는 {num_pages} 페이지가 있습니다.")
            return None
        page = reader.pages[page_number - 1]
        return page.extract_text()
    except Exception as e:
        st.error(f"PDF 텍스트 추출 중 오류 발생: {e}")
        return None

# Streamlit 앱 시작
st.title("PDF 번역기")
st.subheader("PDF 파일의 텍스트를 Google Translate로 번역합니다.")

# PDF 파일 설정
pdf_file_path = "ever3.pdf"

if not os.path.exists(pdf_file_path):
    st.error(f"{pdf_file_path} 파일이 디렉토리에 존재하지 않습니다.")
else:
    # PDF 페이지 번호 입력
    page_number = st.number_input("번역할 페이지 번호를 입력하세요.", min_value=1, step=1)

    if st.button("번역 시작"):
        # PDF 텍스트 추출
        extracted_text = extract_text_from_pdf(pdf_file_path, page_number)
        if extracted_text:
            st.text("추출된 텍스트:")
            st.write(extracted_text)

            # 텍스트 번역
            translated_text = translate_text(extracted_text)
            if translated_text:
                st.text("번역된 텍스트:")
                st.write(translated_text)

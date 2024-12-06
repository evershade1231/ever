import streamlit as st
from PyPDF2 import PdfReader
import requests

# 번역 API 호출 함수
def translate_text(text, target_language="ko"):
    api_key = "AIzaSyCk7EoNf3sVvEkOoB6ChghxJ2q2URQnW90"  # Google Cloud API 키
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"q": text, "target": target_language, "key": api_key}
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    else:
        return f"번역 오류: {response.status_code}"

# PDF에서 텍스트 추출 함수
def extract_text_from_pdf(file, page_number):
    reader = PdfReader(file)
    if page_number <= len(reader.pages):
        return reader.pages[page_number - 1].extract_text()
    else:
        return "해당 페이지가 없습니다."

# Streamlit 앱 인터페이스
st.title("PDF 번역기")
st.subheader("PDF 파일에서 텍스트를 추출하고 번역합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

# 페이지 번호 입력
page_number = st.number_input("번역할 페이지 번호", min_value=1, step=1)

# 번역 버튼
if st.button("번역 시작"):
    if uploaded_file is not None:
        with st.spinner("번역 중... 잠시만 기다려 주세요."):
            # 텍스트 추출
            extracted_text = extract_text_from_pdf(uploaded_file, page_number)
            st.write("### 추출된 텍스트:")
            st.text(extracted_text)

            # 번역 수행
            if extracted_text and extracted_text != "해당 페이지가 없습니다.":
                translated_text = translate_text(extracted_text)
                st.write("### 번역된 텍스트:")
                st.text(translated_text)
            else:
                st.error("텍스트를 추출할 수 없습니다.")
    else:
        st.error("PDF 파일을 업로드해주세요.")

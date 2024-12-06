import os
import requests
import streamlit as st
from PyPDF2 import PdfReader
from google.cloud import translate_v2 as translate

# Google Cloud JSON 키 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Google Translate API 클라이언트 생성
def translate_text(text, target_language="ko"):
    try:
        client = translate.Client()
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        st.error(f"번역 오류 발생: {e}")
        return None

# PDF 파일에서 텍스트 추출 함수
def extract_text_from_pdf(file, page_number):
    try:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        if page_number > num_pages or page_number < 1:
            st.error(f"유효하지 않은 페이지 번호입니다. PDF에는 {num_pages}페이지가 있습니다.")
            return None
        page = reader.pages[page_number - 1]
        return page.extract_text()
    except Exception as e:
        st.error(f"PDF 텍스트 추출 중 오류 발생: {e}")
        return None

# GitHub에서 PDF 파일 다운로드
def fetch_pdf_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.success("GitHub에서 PDF 파일을 성공적으로 불러왔습니다.")
            return response.content
        else:
            st.error(f"PDF 파일을 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"GitHub에서 파일 가져오기 중 오류 발생: {e}")
        return None

# Streamlit 앱
st.title("PDF 번역기")
st.subheader("PDF 파일에서 텍스트를 추출하고 Google Translate를 통해 번역합니다.")

# PDF 파일 선택 옵션
option = st.radio("PDF 파일 선택 방법:", ["직접 업로드", "GitHub에서 가져오기"])

# GitHub PDF URL
GITHUB_PDF_URL = "https://github.com/evershade1231/ever/raw/refs/heads/main/ever3.pdf"

uploaded_file = None

if option == "직접 업로드":
    # 파일 업로드 옵션
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type="pdf")
elif option == "GitHub에서 가져오기":
    # GitHub에서 PDF 파일 가져오기
    if st.button("GitHub에서 PDF 가져오기"):
        pdf_data = fetch_pdf_from_github(GITHUB_PDF_URL)
        if pdf_data:
            with open("temp.pdf", "wb") as f:
                f.write(pdf_data)
            uploaded_file = "temp.pdf"

# 페이지 번호 입력
page_number = st.number_input("번역할 페이지 번호를 입력하세요.", min_value=1, step=1)

if st.button("번역 시작"):
    if uploaded_file is not None:
        # PDF 텍스트 추출
        extracted_text = extract_text_from_pdf(uploaded_file, page_number)
        if extracted_text:
            st.text("추출된 텍스트:")
            st.write(extracted_text)

            # 텍스트 번역
            translated_text = translate_text(extracted_text)
            if translated_text:
                st.text("번역된 텍스트:")
                st.write(translated_text)
    else:
        st.error("PDF 파일을 선택하거나 업로드해주세요.")

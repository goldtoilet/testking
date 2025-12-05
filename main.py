import os
import base64
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ==== .env 로드 ====
load_dotenv()

# ==== 환경변수에서 키 읽기 ====
API_KEY = os.getenv("GPT_API_KEY", "")

st.set_page_config(page_title="OpenAI 키 체크", page_icon="🗝️", layout="centered")

st.title("🔐 OpenAI API 키 체크 도구")

if not API_KEY:
    st.error("GPT_API_KEY 환경변수가 설정되어 있지 않습니다. .env 또는 Streamlit 환경변수를 확인해주세요.")
    st.stop()

# 키 일부만 보여주기 (보안)
masked = API_KEY[:7] + "..." + API_KEY[-4:]
st.info(f"현재 사용 중인 GPT_API_KEY: `{masked}`")

client = OpenAI(api_key=API_KEY)

st.markdown("---")

# ==== 1) 텍스트 API 테스트 ====
st.subheader("1️⃣ 텍스트(Chat) API 테스트")

if st.button("텍스트 테스트 실행", type="primary"):
    try:
        with st.spinner("텍스트 모델 호출 중..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": "이 문장은 OpenAI API 키가 정상 동작하는지 테스트하는 문장입니다. 한 줄로만 대답해줘.",
                    }
                ],
            )
        content = resp.choices[0].message.content
        st.success("✅ 텍스트 API 호출 성공!")
        st.write("**응답:**")
        st.write(content)
    except Exception as e:
        st.error("❌ 텍스트 API 호출 중 오류가 발생했습니다.")
        st.exception(e)

st.markdown("---")

# ==== 2) 이미지 API 테스트 ====
st.subheader("2️⃣ 이미지 API 테스트")

st.caption("gpt-image-1, 1024x1024, quality='low' 로 아주 간단한 테스트 이미지를 생성합니다.")

if st.button("이미지 테스트 실행", type="secondary"):
    try:
        with st.spinner("이미지 모델 호출 중..."):
            img_resp = client.images.generate(
                model="gpt-image-1",
                prompt="simple flat blue square in the center on white background, minimal test image",
                size="1024x1024",
                quality="low",
                n=1,
            )

        b64 = img_resp.data[0].b64_json
        img_bytes = base64.b64decode(b64)

        st.success("✅ 이미지 API 호출 성공!")
        st.image(img_bytes, caption="테스트 이미지 (gpt-image-1)", use_container_width=True)

    except Exception as e:
        st.error("❌ 이미지 API 호출 중 오류가 발생했습니다.")
        st.exception(e)

st.markdown("---")
st.caption("위에서 텍스트는 되는데 이미지에서만 PermissionDeniedError가 난다면, 계정의 이미지 모델 권한/프로젝트 설정 문제일 가능성이 높습니다.")

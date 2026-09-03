import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("冷蔵庫レシピ提案アプリ")
st.write("冷蔵庫の中身を撮影してアップロードすると、AIがレシピを提案します。")

uploaded_file = st.file_uploader("冷蔵庫の写真をアップロード", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_container_width=True)

    if st.button("レシピを提案してもらう"):
        with st.spinner("AIが冷蔵庫の中身を確認中..."):
            model = genai.GenerativeModel("gemini-3.6-flash")

            ingredient_prompt = "この画像に写っている食材を、日本語でリスト形式（例：卵、玉ねぎ、豚肉）で挙げてください。食材以外のものは無視してください。"
            ingredient_response = model.generate_content([ingredient_prompt, image])
            ingredients = ingredient_response.text

            st.subheader("認識された食材")
            st.write(ingredients)

        with st.spinner("レシピを考え中..."):
            recipe_prompt = "以下の食材を使って作れる、簡単で時短なレシピを2つ提案してください。主婦や一人暮らしの人向けに、分かりやすく書いてください。食材: " + ingredients

            recipe_response = model.generate_content(recipe_prompt)

            st.subheader("提案レシピ")
            st.write(recipe_response.text)



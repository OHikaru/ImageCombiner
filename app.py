import streamlit as st
from PIL import Image
import io

def combine_images(images):
    widths, heights = zip(*(i.size for i in images))
    max_height = max(heights)
    total_width = sum(widths)
    
    combined_image = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]
    
    return combined_image

st.title("画像結合アプリ")

uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]
    
    if st.button("画像を結合"):
        combined_image = combine_images(images)
        st.image(combined_image, caption="結合された画像", use_column_width=True)
        
        buf = io.BytesIO()
        combined_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="結合画像をダウンロード",
            data=byte_im,
            file_name="combined_image.png",
            mime="image/png"
        )
else:
    st.write("画像をアップロードしてください。")

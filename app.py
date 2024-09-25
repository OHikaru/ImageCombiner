import streamlit as st
from PIL import Image
import io

def combine_images(images, direction='horizontal'):
    if direction == 'horizontal':
        widths, heights = zip(*(i.size for i in images))
        max_height = max(heights)
        total_width = sum(widths)
        combined_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.size[0]
    else:  # vertical
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)
        combined_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in images:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.size[1]
    
    return combined_image

st.title("画像結合アプリ")

uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]
    
    direction = st.radio(
        "結合方向を選択してください",
        ('水平', '垂直')
    )
    
    if st.button("画像を結合"):
        combined_image = combine_images(images, 'horizontal' if direction == '水平' else 'vertical')
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

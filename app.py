import streamlit as st
from PIL import Image
import io

def resize_image(image, target_size, direction):
    """画像のアスペクト比を保ちながらリサイズする"""
    original_width, original_height = image.size
    if direction == 'horizontal':
        # 高さを合わせる
        new_height = target_size
        new_width = int(original_width * (new_height / original_height))
    else:  # vertical
        # 幅を合わせる
        new_width = target_size
        new_height = int(original_height * (new_width / original_width))
    
    return image.resize((new_width, new_height), Image.LANCZOS)

def combine_images(images, direction='horizontal'):
    if direction == 'horizontal':
        max_height = max(img.size[1] for img in images)
        resized_images = [resize_image(img, max_height, 'horizontal') for img in images]
        total_width = sum(img.size[0] for img in resized_images)
        combined_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in resized_images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.size[0]
    else:  # vertical
        max_width = max(img.size[0] for img in images)
        resized_images = [resize_image(img, max_width, 'vertical') for img in images]
        total_height = sum(img.size[1] for img in resized_images)
        combined_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in resized_images:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.size[1]
    
    return combined_image

st.title("画像結合アプリ")

uploaded_files = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]
    
    direction = st.radio(
        "結合方向を選択してください",
        ('垂直','水平')
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

st.write("""
### 画像サイズの調整について
- 水平方向に結合する場合：すべての画像の高さが最も高い画像に合わせて調整されます。
- 垂直方向に結合する場合：すべての画像の幅が最も幅の広い画像に合わせて調整されます。
- いずれの場合も、画像の縦横比は保持されます。
""")

from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SERVER_ADDRESS')
port = os.getenv('SERVER_PORT')
model_path = os.getenv('MODEL_PATH')
img_path = os.getenv('IMG_PATH')

model = tf.keras.models.load_model(model_path)



def prepare_img(image):
    image  = tf.keras.preprocessing.image.smart_resize(image, (128, 128))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = np.reshape(image_array, (1,128, 128,3))
    image_array = image_array/255.0
    return image_array
app = Flask(__name__)
CORS(app)
@app.route('/predict' , methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': '이미지 파일이 없습니다.'}), 400

    file = request.files['file']
    try:
        # 파일 읽기
        file.save(img_path+file.filename)
        image = tf.keras.utils.load_img(img_path+file.filename)
        result = model.predict(prepare_img(image))
        print(result)

        result_idx = np.argmax(result)
        result_idx = int(result_idx)
        probability = f"{np.max(result):.2%}"
        print(probability) # 내일 제이슨으로 보내기
        result_str  = ""
        os.remove(img_path+file.filename)
        if result_idx == 0:
            result_str = '마들렌'
        elif result_idx == 1:
            result_str = '두쫀쿠'
        elif result_idx == 2:
            result_str = '말차시루'
        else:
            return jsonify({'error': '서버내부 오류'}), 500

        return jsonify({'result': result_str, 'probability': probability}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    print(f"=== 현재 설정된 IP: {server} / 포트: {port} ===")
    app.run(host=server, port=port)





# Authors: Robert Layton <robertlayton@gmail.com>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Mathieu Blondel <mathieu@mblondel.org>
#
# License: BSD 3 clause

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from flask import Flask, jsonify, request
from PIL import Image
import os,io


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        n_colors = 64
        file = request.files['file']
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        china = np.array(img, dtype=np.float64) / 255
        
        w, h, d = original_shape = tuple(china.shape)
        assert d == 3
        image_array = np.reshape(china, (w * h, d))

        image_array_sample = shuffle(image_array, random_state=0, n_samples=1_000)
        kmeans = KMeans(n_clusters=n_colors, n_init="auto", random_state=0).fit(
            image_array_sample
        )

        return_centers = {}
        cluster_centers = kmeans.cluster_centers_*255
        for i in range(len(kmeans.cluster_centers_)):
            return_centers[i] = cluster_centers[i].tolist()
        return jsonify(return_centers)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 11411))
    app.run(debug=True, host='0.0.0.0', port=port)

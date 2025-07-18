from flask import Flask, request, render_template_string
import boto3

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'ec2-upload-bucket-<your-unique-id>'  # Replace with actual bucket name

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>S3 File Uploader</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #a1c4fd, #c2e9fb);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 30px 50px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            text-align: center;
        }
        h2 {
            color: #2b2b2b;
        }
        input[type="file"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        input[type="submit"] {
            padding: 10px 30px;
            background-color: #007bff;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .message {
            margin-top: 20px;
            color: green;
            font-weight: bold;
        }
        footer {
            position: fixed;
            bottom: 10px;
            font-size: 14px;
            color: #444;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload File to S3</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <input type="submit" value="Upload">
        </form>
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}
    </div>
    <footer>Project by Rohan Singh Chouhan</footer>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    message = ''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)
            message = f"Uploaded '{file.filename}' to S3 bucket."
    return render_template_string(HTML, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

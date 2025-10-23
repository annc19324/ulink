from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<filename>')
def serve_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(debug=True)

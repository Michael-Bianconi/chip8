from flask import Flask, render_template, send_from_directory
import sys, os
SRC_DIR = 'src'
BUILD_DIR = 'build'
app = Flask(__name__, template_folder=BUILD_DIR)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # no caching TODO remove me


def build() -> None:
    print('BUILDING...')
    print('COMPILING TYPESCRIPT...')
    #os.system('tsc')
    print('COMPILING HTML...')
    os.system(f'cp {SRC_DIR}/*.html {BUILD_DIR}')
    print('COMPILING CSS...')
    os.system(f'cp {SRC_DIR}/*.css {os.path.join(BUILD_DIR, "css")}')
    print('DONE')


build()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/js/<path:filename>')
def serve_static_js(filename):
    return send_from_directory(os.path.join('.', 'build', 'js'), filename)


@app.route('/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory(os.path.join('.', 'build', 'css'), filename)
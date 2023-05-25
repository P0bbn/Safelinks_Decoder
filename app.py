from flask import Flask, render_template, request, redirect, url_for
import urllib.parse
from datetime import datetime
import re

app = Flask(__name__)

session_history = []

def is_safelinks_encoded(link):
    parsed_url = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    return 'url' in query_params

def decode_safelinks(link):
    parsed_url = urllib.parse.urlparse(link)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    decoded_link = query_params.get('url', [''])[0]
    decoded_link = urllib.parse.unquote(decoded_link)
    return decoded_link

def get_redirect_link(link):
    # Add your logic to determine if the link contains a redirect
    # For demonstration purposes, let's assume a simple regex pattern to detect redirects
    pattern = r"redirect=(\S+)"
    match = re.search(pattern, link)
    if match:
        redirect_link = match.group(1)
        return redirect_link
    return None

@app.route('/', methods=['GET', 'POST'])
def decode_form():
    global session_history

    if request.method == 'POST':
        safelinks_link = request.form['safelinks_link']
        original_link = decode_safelinks(safelinks_link)
        session_history.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), original_link))
        if len(session_history) > 5:
            session_history = session_history[-5:]

        return render_template('index.html', message='Decoding successful.', original_link=original_link,
                               session_history=session_history)

    elif request.method == 'GET':
        return render_template('index.html', session_history=session_history)


@app.route('/clear_history', methods=['POST'])
def clear_history():
    global session_history
    session_history = []
    return redirect(url_for('decode_form'))


if __name__ == '__main__':
    app.run()

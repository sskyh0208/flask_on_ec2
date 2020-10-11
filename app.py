# encoding: utf-8
from flaskr import create_app

# windows時のみ
# import locale
# locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

app = create_app()

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run()
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from conversions import c_to_f, f_to_c, c_to_k, k_to_c, validate_temperature
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = "change_this_secret_in_production"
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json() or {}
    value = data.get('value')
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')

    # server-side validation
    error = validate_temperature(value, from_unit)
    if error:
        return jsonify({'success': False, 'message': error}), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'invalid numeric value'}), 400

    # convert via celsius as intermediate
    if from_unit == to_unit:
        result = value
    else:
        # normalize to celsius
        if from_unit == 'c':
            c = value
        elif from_unit == 'f':
            c = f_to_c(value)
        elif from_unit == 'k':
            c = k_to_c(value)
        else:
            return jsonify({'success': False, 'message': 'unsupported unit'}), 400

        # convert celsius to target
        if to_unit == 'c':
            result = c
        elif to_unit == 'f':
            result = c_to_f(c)
        elif to_unit == 'k':
            result = c_to_k(c)
        else:
            return jsonify({'success': False, 'message': 'unsupported unit'}), 400

    # rounding for display
    result = round(result, 4)
    return jsonify({'success': True, 'result': result, 'from_unit': from_unit, 'to_unit': to_unit})

if __name__ == '__main__':
    app.run(debug=True)

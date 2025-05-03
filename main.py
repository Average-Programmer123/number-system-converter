from flask import Flask, render_template, request

app = Flask(__name__)

# Roman Numeral Conversion Helper Function
def to_roman(n):
    roman_numerals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]
    result = ""
    for value, numeral in roman_numerals:
        while n >= value:
            result += numeral
            n -= value
    return result

# Function to convert decimal to other formats
def convert_decimal(decimal):
    binary = bin(decimal)[2:]
    hexadecimal = hex(decimal)[2:]
    octal = oct(decimal)[2:]
    scientific = "{:.2e}".format(decimal)
    roman = to_roman(decimal)
    text = ''.join([chr(int(decimal)) if 32 <= int(decimal) <= 126 else '' for decimal in str(decimal).split()])
    return binary, hexadecimal, octal, scientific, roman, text


def text_to_decimala(text):
    return ' '.join(str(ord(c)) for c in text)

def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def get_conversion_steps(decimal, base):
    steps = []
    n = decimal
    while n > 0:
        quotient = n // base
        remainder = n % base
        steps.append({
            'n': n,
            'quotient': quotient,
            'remainder': remainder
        })
        n = quotient
    return steps

# Store conversion history in-memory
history = []

@app.route('/', methods=['GET', 'POST'])
def home():
    decimal_result = ""
    binary_result = ""
    hex_result = ""
    octal_result = ""
    scientific_result = ""
    roman_result = ""
    text_result = ""
    reverse_ascii_result = ""
    error_message = ""

    binary_steps = []
    octal_steps = []
    hex_steps = []

    if request.method == 'POST':
        decimal_input = request.form['decimal']
        text_input = request.form.get('text')
        if decimal_input.isdigit():
            decimal = int(decimal_input)
            binary_result, hex_result, octal_result, scientific_result, roman_result, text_result = convert_decimal(decimal)
            decimal_result = decimal_input
            reverse_ascii_result = text_to_decimala(text_input) if text_input else ""
            bin_text = text_to_binary(text_input)

            binary_steps = get_conversion_steps(decimal, 2)
            octal_steps = get_conversion_steps(decimal, 8)
            hex_steps = get_conversion_steps(decimal, 16)

            history.append({
                'decimal': decimal,
                'binary': binary_result,
                'hexadecimal': hex_result,
                'octal': octal_result,
                'scientific': scientific_result,
                'roman': roman_result,
                'text': text_result,
                'reverse_ascii': reverse_ascii_result,
                'bin_text':bin_text
            })
            if len(history) > 5:
                history.pop(0)
        else:
            error_message = "Please enter a valid decimal number."

    return render_template('index.html',
                           decimal_result=decimal_result,
                           binary_result=binary_result,
                           hex_result=hex_result,
                           octal_result=octal_result,
                           scientific_result=scientific_result,
                           roman_result=roman_result,
                           text_result=text_result,
                           reverse_ascii_result=reverse_ascii_result,
                           bin_text = bin_text,
                           error_message=error_message,
                           history=history,
                           binary_steps=binary_steps,
                           octal_steps=octal_steps,
                           hex_steps=hex_steps)

if __name__ == "__main__":
    app.run(debug=True)

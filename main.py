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
    bin_text = ""

    binary_steps = []
    octal_steps = []
    hex_steps = []

    # Variables for the sum and conversion results from the form
    sum_result = None
    a = b = c = ""

    if request.method == 'POST':
            decimal_input = request.form.get('decimal', '').strip()
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
            optc =  request.form.get('oper')
            whtt = request.form.get('wht')
            if whtt == "Decimal":
                try:
                    num1 = float(request.form.get('num1', ''))
                    num2 = float(request.form.get('num2', ''))
                    
                    if optc == "Add":
                        sum_result = num1 + num2
                        a = hex(int(sum_result))[2:]
                        b = bin(int(sum_result))[2:]
                        c = oct(int(sum_result))[2:]
                        d = sum_result
                    elif optc == "Subtract":
                        sum_result = num1 - num2
                        a = hex(int(sum_result))[2:]
                        b = bin(int(sum_result))[2:]
                        c = oct(int(sum_result))[2:]
                        d = sum_result
                    elif optc == "Multiply":
                        sum_result = num1 * num2
                        a = hex(int(sum_result))[2:]
                        b = bin(int(sum_result))[2:]
                        c = oct(int(sum_result))[2:]
                        d = sum_result
                    elif optc == "Divide":
                        sum_result = num1 / num2
                        a = hex(int(sum_result))[2:]
                        b = bin(int(sum_result))[2:]
                        c = oct(int(sum_result))[2:]
                        d = sum_result
                except ValueError:
                        sum_result = "Please enter valid numbers."
            elif whtt == "Binary":
                    num1_raw = request.form.get('num1', '').strip()
                    num2_raw = request.form.get('num2', '').strip()
                    optc = request.form.get('oper')

                    # Try interpreting both numbers as binary
                    try:
                        num1 = int(num1_raw, 2)
                        num2 = int(num2_raw, 2)

                        if optc == "Add":
                            result = num1 + num2
                        elif optc == "Subtract":
                            result = num1 - num2
                        elif optc == "Multiply":
                            result = num1 * num2
                        elif optc == "Divide":
                            result = num1 / num2  # Float division to preserve precision

                        sum_result = result
                        a = hex(int(result))[2:]
                        b = bin(int(result))[2:]
                        c = oct(int(result))[2:]
                        d = result

                    except ValueError:
                        sum_result = "Invalid binary input. Please enter valid binary numbers (e.g., 1010)."
            elif whtt == "Hexadecimal":
                    num1_raw = request.form.get('num1', '').strip()
                    num2_raw = request.form.get('num2', '').strip()
                    optc = request.form.get('oper')

                    # Try interpreting both numbers as binary
                    try:
                        num1 = int(num1_raw, 16)
                        num2 = int(num2_raw, 16)

                        if optc == "Add":
                            result = num1 + num2
                        elif optc == "Subtract":
                            result = num1 - num2
                        elif optc == "Multiply":
                            result = num1 * num2
                        elif optc == "Divide":
                            result = num1 / num2  # Float division to preserve precision

                        sum_result = result
                        a = hex(int(result))[2:]
                        b = bin(int(result))[2:]
                        c = oct(int(result))[2:]
                        d = result

                    except ValueError:
                        sum_result = "Invalid binary input. Please enter valid binary numbers (e.g., 1A)."
                        
            elif whtt == "Octal":
                    num1_raw = request.form.get('num1', '').strip()
                    num2_raw = request.form.get('num2', '').strip()
                    optc = request.form.get('oper')

                    # Try interpreting both numbers as binary
                    try:
                        num1 = int(num1_raw, 8)
                        num2 = int(num2_raw, 8)

                        if optc == "Add":
                            result = num1 + num2
                        elif optc == "Subtract":
                            result = num1 - num2
                        elif optc == "Multiply":
                            result = num1 * num2
                        elif optc == "Divide":
                            result = num1 / num2  # Float division to preserve precision

                        sum_result = result
                        a = hex(int(result))[2:]
                        b = bin(int(result))[2:]
                        c = oct(int(result))[2:]
                        d = result

                    except ValueError:
                        sum_result = "Invalid binary input. Please enter valid binary numbers (e.g., 1010)."

            # Save conversion history
            history.append({
                'decimal': decimal_input,
                'binary': binary_result,
                'hexadecimal': hex_result,
                'octal': octal_result,
                'scientific': scientific_result,
                'roman': roman_result,
                'text': text_result,
                'reverse_ascii': reverse_ascii_result,
                'bin_text': bin_text
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
                           bin_text=bin_text,
                           error_message=error_message,
                           history=history,
                           binary_steps=binary_steps,
                           octal_steps=octal_steps,
                           hex_steps=hex_steps,
                           sum_result=sum_result, a=a, b=b, c=c, d=d)


if __name__ == "__main__":
    app.run(debug=True)

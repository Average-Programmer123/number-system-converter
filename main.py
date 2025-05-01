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
    binary = bin(decimal)[2:]  # Remove the "0b" prefix
    hexadecimal = hex(decimal)[2:]  # Remove the "0x" prefix
    octal = oct(decimal)[2:]  # Remove the "0o" prefix
    scientific = "{:.2e}".format(decimal)
    roman = to_roman(decimal)
    text = ''.join([chr(int(decimal)) if 32 <= int(decimal) <= 126 else '' for decimal in str(decimal).split()])
    return binary, hexadecimal, octal, scientific, roman, text

# Reverse ASCII Helper Function
def text_to_decimal(text):
    return ' '.join(str(ord(c)) for c in text)

# Store conversion history in-memory
history = []

@app.route('/', methods=['GET', 'POST'])
def home():
    binary_result = ""
    hex_result = ""
    octal_result = ""
    scientific_result = ""
    roman_result = ""
    text_result = ""
    error_message = ""
    reverse_ascii_result = ""
    
    if request.method == 'POST':
        decimal_input = request.form['decimal']
        text_input = request.form.get('text')
        
        # Check if decimal input is valid
        if decimal_input.isdigit():
            decimal = int(decimal_input)
            binary_result, hex_result, octal_result, scientific_result, roman_result, text_result = convert_decimal(decimal)
            reverse_ascii_result = text_to_decimal(text_input) if text_input else ""
            
            # Add to history
            history.append({
                'decimal': decimal,
                'binary': binary_result,
                'hexadecimal': hex_result,
                'octal': octal_result,
                'scientific': scientific_result,
                'roman': roman_result,
                'text': text_result,
                'reverse_ascii': reverse_ascii_result
            })
            
            # Keep history to the latest 5 entries
            if len(history) > 5:
                history.pop(0)
                
        else:
            error_message = "Please enter a valid decimal number."
    
    return render_template('index.html', 
                           binary_result=binary_result, 
                           hex_result=hex_result, 
                           octal_result=octal_result,
                           scientific_result=scientific_result,
                           roman_result=roman_result,
                           text_result=text_result,
                           reverse_ascii_result=reverse_ascii_result,
                           error_message=error_message,
                           history=history)

if __name__ == "__main__":
    app.run(debug=True)

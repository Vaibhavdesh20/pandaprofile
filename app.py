from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload_excel.html')

@app.route('/upload-excel', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        try:
            # Save uploaded Excel file
            file.save(file.filename)
            
            # Convert Excel to CSV
            csv_data = convert_excel_to_csv(file.filename)

            from io import StringIO
            # Generate Pandas Profiling report
            df = pd.read_csv(StringIO(csv_data))
            profile = ProfileReport(df)
            profile.to_file("pandas_profiling_report.html")
            
            return jsonify({'success': 'File converted and profiling report generated'})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'File format not supported'})


def convert_excel_to_csv(excel_file):
    # Read Excel file into pandas DataFrame
    df = pd.read_excel(excel_file)
    # Convert DataFrame to CSV string
    csv_data = df.to_csv(index=False)
    return csv_data


if __name__ == '__main__':
    app.run(debug=True)

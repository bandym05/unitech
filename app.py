from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Read CSV file
data = pd.read_csv('synthetic_fraud_detection_data (1).csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    # Geographic Distribution of Fraud Transactions
    fraud_data = data[data['Fraudulent'] == 1]
    city_data = fraud_data.groupby('Merchant Location').size().reset_index(name='Counts')
    city_data['Longitude'] = [18.4233, 25.7479, 28.6139, 31.5204, 27.5894]  # Dummy longitude
    city_data['Latitude'] = [-33.9189, -25.4484, -33.9258, -29.8587, -26.1952]  # Dummy latitude
    
    city_chart = plt.figure()
    plt.scatter(city_data['Longitude'], city_data['Latitude'], s=city_data['Counts']*10, alpha=0.5)
    plt.title('Geographic Distribution of Fraud Transactions')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    city_chart_base64 = base64.b64encode(img.getvalue()).decode()
    
    # Transaction Trends
    trends_data = data.groupby('Transaction Time').size().reset_index(name='Counts')
    trends_chart = plt.figure()
    plt.plot(trends_data['Transaction Time'], trends_data['Counts'])
    plt.title('Transaction Trends')
    plt.xlabel('Date')
    plt.ylabel('Number of Transactions')
    plt.grid(True)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    trends_chart_base64 = base64.b64encode(img.getvalue()).decode()
    
    # Fraud Rate Over Time
    fraud_rate_data = data.groupby('Transaction Time')['Fraudulent'].mean().reset_index(name='Fraud Rate')
    fraud_rate_chart = plt.figure()
    plt.bar(fraud_rate_data['Transaction Time'], fraud_rate_data['Fraud Rate'])
    plt.title('Fraud Rate Over Time')
    plt.xlabel('Date')
    plt.ylabel('Fraud Rate')
    plt.grid(True)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    fraud_rate_chart_base64 = base64.b64encode(img.getvalue()).decode()
    
    return jsonify({
        'city_chart': f'data:image/png;base64,{city_chart_base64}',
        'trends_chart': f'data:image/png;base64,{trends_chart_base64}',
        'fraud_rate_chart': f'data:image/png;base64,{fraud_rate_chart_base64}',
    })

if __name__ == '__main__':
    app.run(debug=True)

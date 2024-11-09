from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'plan': 'Premium',
        'notifications': 3
    }
    energy_data = {
        'daily': {'value': 10, 'unit': 'kWh'},
        'weekly': {'value': 70, 'unit': 'kWh'},
        'monthly': {'value': 300, 'unit': 'kWh'},
        'currentUsage': '15kWh',
        'peakTime': 'Afternoon',
        'recommendations': ['Switch to LED lights', 'Optimize HVAC']
    }
    consumption_data = [
        {'time': 'Mon', 'kwh': 0},
        {'time': 'Tue', 'kwh': 2},
        {'time': 'Wed', 'kwh': 1},
        {'time': 'Thu', 'kwh': 3},
        {'time': 'Fri', 'kwh': 2}
    ]
    return render_template('dashboard.html', user_data=user_data, energy_data=energy_data, consumption_data=consumption_data)

if __name__ == '__main__':
    app.run(debug=True)

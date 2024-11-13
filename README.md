# GreenMax Energy Monitoring System

## Overview
GreenMax is an intelligent energy monitoring system that helps users track, analyze, and optimize their energy consumption using AI-powered recommendations and real-time monitoring.

## Features
- Real-time energy consumption monitoring
- AI-powered usage predictions and recommendations
- Interactive dashboard with usage analytics
- Device-level energy tracking
- Smart notifications for usage anomalies
- Historical data analysis and trends
- Cost optimization suggestions

## Tech Stack
- **Backend**: Python/Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI/ML**: TensorFlow, NumPy
- **Database**: Firebase Realtime Database
- **Authentication**: Firebase Auth
- **API**: Google Cloud (Gemini AI)
- **Deployment**: Google Cloud App Engine

## Prerequisites
- Python 3.9+
- Google Cloud SDK
- Firebase Account
- Gemini API Key

## Installation
1. Clone the repository:
bash git clone https://github.com/Awakenned1/GreenMax-1.git cd GreenMax-1


2. Create virtual environment:
bash python -m venv venv source venv/bin/activate # Linux/Mac .\venv\Scripts\activate # Windows


3. Install dependencies:
bash pip install -r requirements.txt


4. Set up environment variables in `.env`:
env FLASK_SECRET_KEY=your-secret-key GOOGLE_API_KEY=your-google-api-key FIREBASE_API_KEY=your-firebase-api-key

Add other required environment variables

## Project Structure
GreenMax-1/ ├── app/ │ ├── static/ │ │ ├── css/ │ │ ├── js/ │ │ └── images/ │ ├── templates/ │ ├── services/ │ │ ├── energy_monitor.py │ │ ├── data_generator.py │ │ └── auth.py │ ├── models/ │ │ └── predictor.py │ └── routes.py ├── models/ │ ├── energy_model/ │ └── scaler.pkl ├── app.yaml ├── requirements.txt ├── run.py └── README.md


## Configuration
1. Set up Firebase:
   - Create a Firebase project
   - Download service account key
   - Update Firebase configuration in `.env`

2. Configure Google Cloud:
   - Enable required APIs
   - Set up App Engine
   - Configure service accounts

## Deployment
1. Initialize Google Cloud:
bash gcloud init


2. Deploy to App Engine:
bash gcloud app deploy


3. View the application:
bash gcloud app browse


## API Endpoints
- `/`: Home page
- `/dashboard`: Main dashboard
- `/api/dashboard-data`: Get real-time dashboard data
- `/api/energy-data`: Get energy consumption data
- `/auth/login`: User login
- `/auth/register`: User registration

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security
- All API keys and sensitive data should be stored in environment variables
- Firebase Authentication is implemented for user security
- HTTPS is enforced for all connections
- Regular security updates and dependency maintenance

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Contact
Your Name - nnkosinam@gmail.com
Project Link: [https://github.com/yourusername/GreenMax-1](https://github.com/Awakenned1/GreenMax-1)

## Acknowledgments
- Google Cloud Platform
- Firebase
- TensorFlow
- Flask Framework
- Chart.js for visualizations
- 
Google Cloud Platform (GCP):
-App Engine for hosting
-Cloud Storage for static files
-Cloud Build for deployment
-Cloud Logging for monitoring
-Firebase Services:
-Firebase Authentication
-Firebase Realtime Database
-Firebase Cloud Messaging (FCM)
-Firebase Storage
-AI/ML Services:
-Google Gemini AI API
-Cloud Functions (optional)
-Additional Services:
-Cloud Secret Manager
-Cloud Monitoring
-Cloud IAM for access control
-Development Tools:
-Google Cloud SDK
-Firebase CLI
-Cloud Shell

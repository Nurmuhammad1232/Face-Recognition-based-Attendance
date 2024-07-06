
# Face-Recognition-based-Attendance

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [License](#license)

## Introduction
The Face-Recognition-based-Attendance system is designed to automate the process of taking attendance using facial recognition technology. It identifies individuals through their facial features and records their attendance in a database. This project utilizes machine learning algorithms and a database for efficient and accurate attendance tracking.

## Features
- Real-time face detection and recognition
- Automatic attendance marking
- User-friendly interface for managing users and attendance records
- Database integration for storing and retrieving attendance data
- Image storage and management

## Prerequisites
- Python 3.6 or higher
- PostgreSQL
- OpenCV
- dlib
- Flask

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/Face-Recognition-based-Attendance.git
   cd Face-Recognition-based-Attendance
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**
   - Create a database named `attendance_db`.
   - Update the database configuration in `postgres/config.py` with your database credentials.


## Usage
1. **Run the application:**
   ```sh
   python main.py
   ```

2. **Open your web browser and navigate to:**
   ```sh
   http://127.0.0.1:5000
   ```

3. **Add users to the system:**
   - Go to the "User" section and register new users by providing their details and images.

4. **Take attendance:**
   - Navigate to the "Camera" section to start the face recognition process and mark attendance.

## Project Structure
```
Face-Recognition-based-Attendance/
│
├── Camera/
│   └── ... (Camera related code and scripts)
├── User/
│   └── ... (User management code and scripts)
├── calculation/
│   └── ... (Attendance calculation scripts)
├── faceRecognition/
│   └── ... (Face recognition algorithms and models)
├── images/
│   └── ... (Sample images and stored user images)
├── postgres/
│   └── config.py (Database configuration)
├── static/
│   └── ... (Static files like CSS, JavaScript)
├── templates/
│   └── ... (HTML templates)
├── utils/
│   └── ... (Utility scripts)
├── main.py (Main application entry point)
├── requirements.txt (Required Python packages)
├── LICENSE (License file)
└── README.md (Project documentation)
```

## Screenshots
![Screenshot 1](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/1.png)
![Screenshot 2](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/2.png)
![Screenshot 3](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/3.png)
![Screenshot 4](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/4.png)
![Screenshot 5](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/5.png)
![Screenshot 6](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/6.png)
![Screenshot 7](https://raw.githubusercontent.com/Nurmuhammad1232/Face-Recognition-based-Attendance/main/images/7.png)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

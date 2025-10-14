# 🎓 Exam Seat Allocator

A modern, intelligent seat allocation system for educational institutions with anti-copying algorithms and multi-subject support.

## ✨ Features

- **Smart Seat Allocation**: Anti-copying algorithms ensure students with same subjects are separated
- **Multi-Subject Support**: Students can be enrolled in multiple subjects
- **PDF Reports**: Generate professional allocation reports
- **Real-time Interface**: Modern React frontend with live updates
- **Multiple Strategies**: Choose between mixed or separated allocation approaches

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python start.py
```

### Frontend Setup
```bash
npm install
npm run dev
```

## 🎯 Usage

1. **Add Subjects**: Create subject codes (e.g., CS301, IT205)
2. **Add Students**: Register students with their subjects
3. **Add Rooms**: Configure exam rooms with capacities
4. **Allocate Seats**: Use smart algorithms to assign seats
5. **Generate Reports**: Download PDF allocation reports

## 🛠 Technology Stack

- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: Flask, Python
- **Database**: MongoDB
- **Reports**: ReportLab PDF generation

## 📊 Allocation Strategies

- **Mixed**: Minimizes room usage, separates same subjects within rooms
- **Separated**: Distributes same subjects across different rooms

## 🎨 Screenshot

Access the application at `http://localhost:5173` after starting both servers.

## 📄 License

MIT License - feel free to use for educational purposes.

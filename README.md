# Academic Performance Analytics System

## 📋 Project Description

A comprehensive student performance tracking system that analyzes grades, attendance, assignment submissions, and generates predictive insights about academic outcomes. The project would include statistical analysis, data visualization, and reporting features suitable for educational institutions.

This repository contains the source code and documentation for the Academic Performance Analytics System project, developed as part of the UE23CS341A course at PES University.

## 🧑‍💻 Development Team (Insight24)

- [@PES2UG23CS183](https://github.com/PES2UG23CS183) - Scrum Master
- [@PES2UG23CS169](https://github.com/PES2UG23CS169) - Developer Team
- [@PES2UG23CS166](https://github.com/PES2UG23CS166) - Developer Team
- [@pes2ug23cs188-oss](https://github.com/pes2ug23cs188-oss) - Developer Team

## 👨‍🏫 Teaching Assistant

- [@nikitha-0704](https://github.com/nikitha-0704)
- [@samwilson129](https://github.com/samwilson129)
- [@harshamogra](https://github.com/harshamogra)

## 👨‍⚖️ Faculty Supervisor

- [@sudeeparoydey](https://github.com/sudeeparoydey)


## 🚀 Getting Started

### Prerequisites
- [List your prerequisites here]

### Installation
**1. Clone the repository**
   ```bash
   git clone https://github.com/pestechnology/PESU_EC_CSE_C_P24_Academic_Performance_Analytics_System_Insight24.git
   cd PESU_EC_CSE_C_P24_Academic_Performance_Analytics_System_Insight24
   ```

**2. Install dependencies**

   a) Backend Dependencies: Run this command inside the backend folder   
   ```bash
   pip install -r requirements.txt
   ```
   b) Frontend Dependencies: Run this command inside the frontend folder
   ```bash
   pip install -r requirements.txt
   ```
      
**3. Run the application**  
   
   a) Start the backend: Navigate to the backend directory
   ```bash
   cd src/backend
   python app.py
   ```
   Backend will start at: http://127.0.0.1:5000
   
   b) Start the frontend: Open another terminal simultaneously and navigate to the frontend directory
   ```bash
   cd src/frontend
   streamlit run dashboard.py
   ```
   Frontend will start at: http://localhost:8501

## 📁 Project Structure

```
PESU_EC_CSE_C_P24_Academic_Performance_Analytics_System_Insight24/
├── src/                 # Source code
├── docs/               # Documentation
├── tests/              # Test files
├── .github/            # GitHub workflows and templates
├── README.md          # This file
└── ...
```

## 🛠️ Development Guidelines

### Branching Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches

### Commit Messages
Follow conventional commit format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test-related changes

### Code Review Process
1. Create feature branch from `develop`
2. Make changes and commit
3. Create Pull Request to `develop`
4. Request review from team members
5. Merge after approval

## 📚 Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## 📄 License

This project is developed for educational purposes as part of the PES University UE23CS341A curriculum.

---


# LuxSCale Interface - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
cd "LuxSCale interface"
pip install -r requirements.txt
```

### Step 2: Start the Server

**Windows:**
```bash
start_server.bat
```

**Linux/Mac:**
```bash
./start_server.sh
```

The server will start on `http://localhost:8001`

### Step 3: Open the Interface

Open `index.html` in your web browser, or serve it:

```bash
python -m http.server 3000
```

Then open: `http://localhost:3000`

---

## 📝 Fill the Form

The form asks for minimal information:

1. **Project Name** (required)
2. **Room Type** (required) - Select from dropdown
3. **Room Dimensions** (required) - Length, Width, Height
4. **Luminaire Count** (required)
5. **Luminaire Power** (required) - in Watts
6. **Luminous Flux OR Efficacy** (one required)
7. **Mounting Height** (required)

Optional fields:
- Company Name
- Manufacturer
- Article Number
- Work Plane Height (defaults to 0.75m)

---

## ✅ What Happens Next

1. System generates report with calculated parameters
2. System checks compliance against standards
3. Results displayed with pass/fail status
4. Download report as JSON file

---

## 📊 Example Input

```
Project Name: Office Building
Room Type: Offices
Room Length: 10.0 m
Room Width: 8.0 m
Room Height: 3.0 m
Luminaire Count: 12
Luminaire Power: 50 W
Efficacy: 100 lm/W
Mounting Height: 2.5 m
```

---

## 🎯 That's It!

The system handles all calculations and compliance checking automatically.

For detailed documentation, see:
- [README.md](README.md) - Overview
- [DOCUMENTATION.md](DOCUMENTATION.md) - Code documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference


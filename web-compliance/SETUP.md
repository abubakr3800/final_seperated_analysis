# Setup Guide - Web Compliance

This guide will help you set up and run the Web Compliance system.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Step 1: Install Python Dependencies

Navigate to the `web-compliance` directory and install required packages:

```bash
cd web-compliance
pip install -r requirements.txt
```

If you encounter permission issues, use:

```bash
pip install --user -r requirements.txt
```

## Step 2: Verify File Structure

Ensure the following files and directories exist:

```
final_comparator/
├── web-compliance/
│   ├── api_server.py
│   ├── compliance_checker.py
│   ├── index.html
│   └── requirements.txt
├── standard_export/
│   └── output/
│       └── standards_filtered.json
└── report_export/
    └── extractors/
        └── aliases.json
```

## Step 3: Start the Report API

The Report API must be running before starting the Compliance API.

### Option A: If Report API is already running
Skip to Step 4.

### Option B: Start Report API manually

```bash
cd ../report_export/api
python api_server.py
```

The Report API should start on `http://localhost:5000`

Verify it's running:
```bash
curl http://localhost:5000/health
```

## Step 4: Start the Compliance API

In a new terminal window:

```bash
cd web-compliance
python api_server.py
```

You should see:
```
🚀 Starting Lighting Compliance Checker API (Web-Compliance)...
============================================================
📋 API Endpoints:
  GET  /                    - API documentation
  GET  /health              - Health check
  ...
🌐 Server will start on http://localhost:8000
📖 API docs available at http://localhost:8000/docs
============================================================
```

## Step 5: Open the Web Interface

### Option A: Direct File Open
Simply open `index.html` in your web browser:
- Double-click `index.html`
- Or right-click → Open with → Browser

### Option B: Local Web Server (Recommended)

Using Python's built-in server:

```bash
cd web-compliance
python -m http.server 3000
```

Then open: `http://localhost:3000`

### Option C: Using Node.js (if installed)

```bash
cd web-compliance
npx http-server -p 3000
```

## Step 6: Test the System

1. **Test API Health**
   - Open browser to `http://localhost:8000/health`
   - Should return JSON with status "healthy"

2. **Test Web Interface**
   - Open `index.html` or `http://localhost:3000`
   - Upload a PDF file
   - Verify results are displayed

## Configuration

### Changing Ports

**Compliance API Port** (default: 8000):
Edit `api_server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to desired port
```

**Report API Port** (default: 5000):
Edit `compliance_checker.py`:
```python
REPORT_API_URL = "http://localhost:5000"  # Change port if needed
```

**Web Interface API URL**:
Edit `index.html`:
```javascript
const API_BASE = 'http://localhost:8000';  // Change to match API port
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Install missing dependencies
```bash
pip install fastapi uvicorn requests
```

### Issue: "Port already in use"

**Solution**: 
1. Find process using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```
2. Kill the process or use a different port

### Issue: "Standards file not found"

**Solution**: Verify the path in `api_server.py`:
```python
STANDARDS_PATH = BASE_DIR / "standard_export" / "output" / "standards_filtered.json"
```

Ensure you're running from the correct directory.

### Issue: "Report API connection failed"

**Solution**:
1. Verify Report API is running: `curl http://localhost:5000/health`
2. Check firewall settings
3. Verify CORS is enabled in Report API

### Issue: Web interface shows "Error: Failed to process file"

**Solution**:
1. Check browser console (F12) for errors
2. Verify API is running: `http://localhost:8000/health`
3. Check API logs for detailed error messages
4. Ensure PDF file is valid and not corrupted

### Issue: "Aliases file not found"

**Solution**: The system will work without aliases, but parameter recognition may be limited. Verify the path:
```python
# In compliance_checker.py
aliases_file = project_root / "report_export" / "extractors" / "aliases.json"
```

## Running in Production

For production deployment:

1. **Use a production ASGI server**:
   ```bash
   pip install gunicorn
   gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Serve static files** with a proper web server (nginx, Apache)

3. **Enable HTTPS** for secure connections

4. **Set up environment variables** for configuration

## Next Steps

- Read [API_USAGE.md](API_USAGE.md) for API usage details
- Check [README.md](README.md) for feature overview
- Test with sample PDF files
- Customize the interface as needed

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs
3. Check browser console for errors
4. Verify all services are running


"""
Quick test to verify all services are working
"""

import requests
import time

def test_endpoint(url, name):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: OK")
            return True
        else:
            print(f"❌ {name}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    print("🧪 Quick Service Test")
    print("=" * 30)
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Test endpoints
    tests = [
        ("http://localhost:5000/health", "Report API"),
        ("http://localhost:8000/health", "Compliance API"),
        ("http://localhost:8000/proxy/report-health", "CORS Proxy"),
        ("http://localhost:8000/standards-info", "Standards")
    ]
    
    results = []
    for url, name in tests:
        results.append(test_endpoint(url, name))
        time.sleep(1)
    
    print("\n" + "=" * 30)
    if all(results):
        print("🎉 All services working!")
        print("🌐 Go to http://localhost:3000 for web interface")
    else:
        print("⚠️  Some services not working")
        print("💡 Try running restart_services.bat")

if __name__ == "__main__":
    main()

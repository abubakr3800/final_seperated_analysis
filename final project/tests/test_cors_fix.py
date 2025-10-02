"""
Test the CORS fix for the web interface
"""

import requests
import json

def test_cors_proxy():
    """Test the CORS proxy endpoint"""
    try:
        response = requests.get("http://localhost:8000/proxy/report-health")
        if response.status_code == 200:
            data = response.json()
            print("✅ CORS Proxy working!")
            print(f"   Report API Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ CORS Proxy failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS Proxy error: {e}")
        return False

def test_direct_report_api():
    """Test direct access to report API"""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Report API accessible directly")
            return True
        else:
            print(f"❌ Report API failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Report API error: {e}")
        return False

def main():
    print("🔧 Testing CORS Fix")
    print("=" * 30)
    
    print("\n1. Testing direct Report API access...")
    direct_ok = test_direct_report_api()
    
    print("\n2. Testing CORS proxy...")
    proxy_ok = test_cors_proxy()
    
    print("\n" + "=" * 30)
    if direct_ok and proxy_ok:
        print("🎉 CORS fix successful!")
        print("💡 Web interface should now work properly")
        print("🌐 Go to http://localhost:3001 to test")
    else:
        print("⚠️  Some issues detected")
        if not direct_ok:
            print("   - Report API not accessible")
        if not proxy_ok:
            print("   - CORS proxy not working")

if __name__ == "__main__":
    main()

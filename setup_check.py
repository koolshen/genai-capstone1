"""
Quick setup verification script.
Checks if all dependencies and configurations are in place.
"""
import os
import sys

def check_database():
    """Check if database exists."""
    if os.path.exists('sales_data.db'):
        print("✅ Database file exists")
        return True
    else:
        print("❌ Database file not found. Run: python database_setup.py")
        return False

def check_env_file():
    """Check if .env file exists."""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            print("✅ OPENAI_API_KEY is set")
            return True
        else:
            print("⚠️  OPENAI_API_KEY not configured in .env")
            return False
    else:
        print("❌ .env file not found. Copy .env.example to .env and configure it.")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required = ['streamlit', 'openai', 'pandas', 'plotly', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing packages: pip install {' '.join(missing)}")
        return False
    return True

def main():
    print("=" * 50)
    print("Setup Verification")
    print("=" * 50)
    print()
    
    deps_ok = check_dependencies()
    print()
    env_ok = check_env_file()
    print()
    db_ok = check_database()
    print()
    
    print("=" * 50)
    if deps_ok and env_ok and db_ok:
        print("✅ All checks passed! You're ready to run the app.")
        print("Start with: streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    print("=" * 50)

if __name__ == "__main__":
    main()


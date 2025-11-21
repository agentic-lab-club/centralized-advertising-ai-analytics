#!/usr/bin/env python3
"""
DEMETRA AI Analytics - Database Setup Script
This script sets up the database for the MVP hackathon project.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def setup_database():
    """Setup database for DEMETRA AI Analytics MVP"""
    print("🚀 DEMETRA AI Analytics - Database Setup")
    print("=" * 50)
    
    try:
        # Import after adding to path
        from app.utils.seeder import seed_all
        
        # Run the seeder
        seed_all()
        
        print("\n✅ Database setup completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Start the backend: python -m uvicorn app.main:app --reload")
        print("   2. Start the frontend: cd ../frontend && npm start")
        print("   3. Open http://localhost:3000 to view the dashboard")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the backend directory and have installed dependencies:")
        print("   poetry install")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("Check your database connection and try again.")

if __name__ == "__main__":
    setup_database()

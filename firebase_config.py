import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from typing import Optional

class FirebaseService:
    def __init__(self):
        self._db: Optional[firestore.Client] = None
        self._app: Optional[firebase_admin.App] = None
        
    def initialize_firebase(self, service_account_path: str = None):
        """
        Initialize Firebase Admin SDK
        
        Args:
            service_account_path: Path to service account JSON file
                                If None, will try to use environment variables
        """
        try:
            if not firebase_admin._apps:
                if service_account_path and os.path.exists(service_account_path):
                    # Initialize with service account file
                    cred = credentials.Certificate(service_account_path)
                    self._app = firebase_admin.initialize_app(cred)
                else:
                    # Initialize with environment variables (for production)
                    # Make sure GOOGLE_APPLICATION_CREDENTIALS is set
                    self._app = firebase_admin.initialize_app()
                
                print("Firebase initialized successfully!")
            else:
                self._app = firebase_admin.get_app()
                print("Firebase already initialized!")
                
            # Initialize Firestore client
            self._db = firestore.client()
            return True
            
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            return False
    
    @property
    def db(self) -> firestore.Client:
        """Get Firestore database client"""
        if self._db is None:
            raise RuntimeError("Firebase not initialized. Call initialize_firebase() first.")
        return self._db
    
    @property
    def auth_client(self):
        """Get Firebase Auth client"""
        if self._app is None:
            raise RuntimeError("Firebase not initialized. Call initialize_firebase() first.")
        return auth
    
    def verify_token(self, id_token: str):
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None

# Global Firebase service instance
firebase_service = FirebaseService()

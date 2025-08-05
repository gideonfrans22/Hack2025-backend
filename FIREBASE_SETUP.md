# Firebase Setup Guide

## Prerequisites
1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Firestore Database in your Firebase project
3. Generate a service account key

## Setup Steps

### 1. Generate Service Account Key
1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Place it in your project root (e.g., `firebase-service-account.json`)
5. **Important**: Add this file to `.gitignore` to keep it secure

### 2. Environment Configuration
1. Copy `.env.example` to `.env`
2. Update the `.env` file with your Firebase configuration:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=./firebase-service-account.json
   FIREBASE_PROJECT_ID=your-project-id
   DEBUG=True
   ```

### 3. Alternative: Using Environment Variables (Production)
Instead of a service account file, you can use environment variables:
- Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your service account file
- Or set individual Firebase environment variables

### 4. Initialize Firestore Database
1. Go to Firebase Console → Firestore Database
2. Click "Create database"
3. Choose "Start in test mode" for development
4. Select your preferred region

### 5. Test Your Setup
Run your FastAPI server:
```bash
uvicorn main:app --reload
```

Visit these endpoints to test:
- `http://localhost:8000/firebase-status` - Check Firebase connection
- `http://localhost:8000/api/v1/users/` - Test Firestore integration
- `http://localhost:8000/docs` - FastAPI interactive documentation

## Security Notes
- Never commit your service account key to version control
- Use environment variables in production
- Consider using Firebase Authentication for user management
- Set up proper Firestore security rules before going to production

## Available Features
- ✅ Firebase Admin SDK integration
- ✅ Firestore database operations
- ✅ User CRUD operations with Firestore
- ✅ Firebase Authentication token verification (ready to use)
- ✅ Error handling and fallback responses

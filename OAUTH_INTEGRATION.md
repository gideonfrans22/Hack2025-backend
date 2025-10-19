# 🔐 OAuth Integration - Kakao & Naver Login

## Overview

The ReadAble platform now supports social login via **Kakao** and **Naver** OAuth providers. This allows users to authenticate using their existing social media accounts without creating separate passwords.

## 🌟 Features

- **Kakao Login**: Authenticate users with Kakao accounts
- **Naver Login**: Authenticate users with Naver accounts
- **Automatic Account Creation**: New users are automatically created on first login
- **Account Linking**: Existing email accounts can be linked with OAuth providers
- **Unified JWT**: All authentication methods return the same JWT token format
- **Profile Updates**: Users can update their profiles after OAuth login

## 📋 API Endpoints

### 1. Kakao Login

**Endpoint**: `POST /api/v1/auth/kakao/login`

**Request Body**:

```json
{
  "access_token": "kakao_oauth_token_from_frontend",
  "kakao_id": "1234567890",
  "email": "user@example.com",
  "nickname": "UserName",
  "profile_image": "https://example.com/profile.jpg"
}
```

**Response**:

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "firestore_document_id",
      "email": "user@example.com",
      "nickname": "UserName",
      "profile_image": "https://example.com/profile.jpg"
    },
    "is_new_user": false
  }
}
```

### 2. Naver Login

**Endpoint**: `POST /api/v1/auth/naver/login`

**Request Body**:

```json
{
  "access_token": "naver_oauth_token_from_frontend",
  "naver_id": "naver_user_id_123",
  "email": "user@naver.com",
  "nickname": "NaverUser",
  "profile_image": "https://naver.com/profile.jpg"
}
```

**Response**:

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "firestore_document_id",
      "email": "user@naver.com",
      "nickname": "NaverUser",
      "profile_image": "https://naver.com/profile.jpg"
    },
    "is_new_user": true
  }
}
```

### 3. Update User Profile

**Endpoint**: `PUT /api/v1/user/profile`

**Headers**:

```
Authorization: Bearer <jwt_token>
```

**Request Body** (all fields optional):

```json
{
  "name": "Updated Name",
  "age": 25,
  "gender": "female",
  "hobby": "reading",
  "nickname": "NewNickname",
  "profile_image": "https://example.com/new-profile.jpg"
}
```

**Response**:

```json
{
  "id": "firestore_document_id",
  "email": "user@example.com",
  "nickname": "NewNickname",
  "name": "Updated Name",
  "profile_image": "https://example.com/new-profile.jpg",
  "oauth_provider": "kakao"
}
```

## 🔄 Authentication Flow

### Kakao Login Flow

```
1. Frontend: User clicks "Login with Kakao"
2. Frontend: Redirects to Kakao OAuth authorization page
3. Kakao: User authorizes the app
4. Frontend: Receives Kakao access_token and user data
5. Frontend: Sends POST request to /api/v1/auth/kakao/login
6. Backend: Validates data and checks if user exists
   - If user exists: Returns existing user with JWT token
   - If new user: Creates account and returns JWT token
7. Frontend: Stores JWT token for subsequent API calls
```

### Naver Login Flow

```
1. Frontend: User clicks "Login with Naver"
2. Frontend: Redirects to Naver OAuth authorization page
3. Naver: User authorizes the app
4. Frontend: Receives Naver access_token and user data
5. Frontend: Sends POST request to /api/v1/auth/naver/login
6. Backend: Validates data and checks if user exists
   - If user exists: Returns existing user with JWT token
   - If new user: Creates account and returns JWT token
7. Frontend: Stores JWT token for subsequent API calls
```

## 💾 Database Schema

### User Document Structure (with OAuth)

```javascript
{
  "email": "user@example.com",
  "name": "User Name",
  "nickname": "UserNickname",
  "age": 25,
  "gender": "male",
  "hobby": "reading",
  "profile_image": "https://example.com/profile.jpg",

  // OAuth specific fields
  "oauth_provider": "kakao",  // 'kakao', 'naver', or null
  "oauth_id": "1234567890",   // Provider-specific user ID

  // Password field (optional for OAuth users)
  "hashed_password": null,     // null for OAuth-only users

  // Timestamps
  "created_at": "2025-10-18T10:00:00Z",
  "updated_at": "2025-10-18T10:00:00Z"
}
```

## 🔧 Implementation Details

### Account Linking Logic

The system handles three scenarios:

1. **New User (OAuth)**:

   - Creates new account with OAuth provider info
   - Sets `is_new_user: true`
   - Requires profile completion (age, gender)

2. **Existing User (Same Email)**:

   - Links OAuth provider to existing account
   - Updates nickname and profile image
   - Sets `is_new_user: false`

3. **Existing OAuth User**:
   - Updates login timestamp
   - Refreshes profile image and nickname
   - Sets `is_new_user: false`

### JWT Token Generation

OAuth logins generate the same JWT token format as regular logins:

```javascript
{
  "sub": "user@example.com",  // User email
  "user_id": "firestore_doc_id",  // Firestore document ID
  "exp": 1729339200  // Expiration timestamp
}
```

## 📱 Frontend Integration Examples

### React/Next.js Example (Kakao)

```javascript
// 1. Install Kakao SDK
// Add to your HTML: <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>

// 2. Initialize Kakao
useEffect(() => {
  if (!window.Kakao.isInitialized()) {
    window.Kakao.init("YOUR_KAKAO_APP_KEY");
  }
}, []);

// 3. Handle Kakao Login
const handleKakaoLogin = () => {
  window.Kakao.Auth.login({
    success: async (authObj) => {
      // Get user info
      window.Kakao.API.request({
        url: "/v2/user/me",
        success: async (response) => {
          // Send to backend
          const result = await fetch(
            "http://your-api.com/api/v1/auth/kakao/login",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                access_token: authObj.access_token,
                kakao_id: response.id.toString(),
                email: response.kakao_account.email,
                nickname: response.properties.nickname,
                profile_image: response.properties.profile_image
              })
            }
          );

          const data = await result.json();
          // Store JWT token
          localStorage.setItem("token", data.data.token);

          // Redirect or update UI
          if (data.data.is_new_user) {
            router.push("/complete-profile");
          } else {
            router.push("/dashboard");
          }
        }
      });
    },
    fail: (err) => {
      console.error("Kakao login failed:", err);
    }
  });
};
```

### React/Next.js Example (Naver)

```javascript
// 1. Initialize Naver Login
const NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID";
const REDIRECT_URI = encodeURIComponent(
  "http://localhost:3000/auth/naver/callback"
);

// 2. Login Button Click
const handleNaverLogin = () => {
  const state = Math.random().toString(36).substring(7);
  localStorage.setItem("naver_state", state);

  const naverLoginUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${state}`;
  window.location.href = naverLoginUrl;
};

// 3. Callback Handler (in /auth/naver/callback page)
useEffect(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  const state = urlParams.get("state");

  if (code && state === localStorage.getItem("naver_state")) {
    // Exchange code for access token (through your backend proxy)
    exchangeCodeForToken(code);
  }
}, []);

const exchangeCodeForToken = async (code) => {
  // Get access token through backend proxy
  const tokenResponse = await fetch("/api/auth/naver/token", {
    method: "POST",
    body: JSON.stringify({ code })
  });
  const { access_token } = await tokenResponse.json();

  // Get user info
  const userResponse = await fetch("https://openapi.naver.com/v1/nid/me", {
    headers: { Authorization: `Bearer ${access_token}` }
  });
  const userData = await userResponse.json();

  // Send to backend
  const result = await fetch("http://your-api.com/api/v1/auth/naver/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      access_token: access_token,
      naver_id: userData.response.id,
      email: userData.response.email,
      nickname: userData.response.nickname,
      profile_image: userData.response.profile_image
    })
  });

  const data = await result.json();
  localStorage.setItem("token", data.data.token);

  if (data.data.is_new_user) {
    router.push("/complete-profile");
  } else {
    router.push("/dashboard");
  }
};
```

## 🧪 Testing

### Test Kakao Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/kakao/login \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "test_kakao_token",
    "kakao_id": "123456789",
    "email": "test@kakao.com",
    "nickname": "KakaoUser",
    "profile_image": "https://example.com/profile.jpg"
  }'
```

### Test Naver Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/naver/login \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "test_naver_token",
    "naver_id": "naver_123",
    "email": "test@naver.com",
    "nickname": "NaverUser",
    "profile_image": "https://example.com/profile.jpg"
  }'
```

### Test Profile Update

```bash
curl -X PUT http://localhost:8000/api/v1/user/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Updated Name",
    "age": 25,
    "gender": "female",
    "nickname": "NewNickname"
  }'
```

## 🔒 Security Considerations

### OAuth Token Validation

**Important**: The current implementation trusts the OAuth tokens from the frontend. For production:

1. **Validate Kakao Token**:

```python
# Add to controller before processing
import requests

def validate_kakao_token(access_token: str, kakao_id: str) -> bool:
    response = requests.get(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if response.status_code == 200:
        data = response.json()
        return str(data['id']) == kakao_id
    return False
```

2. **Validate Naver Token**:

```python
def validate_naver_token(access_token: str, naver_id: str) -> bool:
    response = requests.get(
        'https://openapi.naver.com/v1/nid/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if response.status_code == 200:
        data = response.json()
        return data['response']['id'] == naver_id
    return False
```

### Best Practices

- ✅ **Always validate OAuth tokens** server-side
- ✅ **Use HTTPS** in production
- ✅ **Set appropriate CORS** origins
- ✅ **Implement rate limiting** on OAuth endpoints
- ✅ **Log OAuth login attempts** for security monitoring
- ✅ **Handle token expiration** gracefully
- ✅ **Store minimal user data** from OAuth providers

## 🎉 Summary

The OAuth integration provides:

- ✅ **Easy Social Login** - Users can sign in with Kakao or Naver
- ✅ **Seamless Account Creation** - New users are automatically created
- ✅ **Unified Authentication** - Same JWT token for all login methods
- ✅ **Profile Management** - Users can update their information
- ✅ **Account Linking** - Multiple OAuth providers can link to same email

**Ready for frontend integration!** 🚀

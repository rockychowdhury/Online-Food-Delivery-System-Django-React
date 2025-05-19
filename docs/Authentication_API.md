
# 🔐 Authentication API Documentation

This project uses **JWT-based authentication** with **HTTP-only cookies** to secure user sessions. Below is a detailed list of all available authentication-related API endpoints.

---

## 📌 Base URL
```
/user/
```

---

### 1. **Register a New User**
`POST /user/register/`

#### Request Body (JSON):
```json
{
  "email": "user@example.com",
  "password": "strongpassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Response:
- `201 Created`
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

---

### 2. **Login User & Set Cookies**
`POST /user/token/`

#### Request Body:
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

#### Response:
- `200 OK`
```json
{
  "message": "Login successful"
}
```

> ⚠️ Both `access_token` and `refresh_token` are sent as **HTTP-only cookies**.

---

### 3. **Access User Profile**
`GET /user/`

- Requires: `access_token` cookie
- Auth Required: ✅

#### Response:
- `200 OK`
```json
{
  "email": "user@example.com",
  "role": "user",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": null,
  "photoURL": null
}
```

---

### 4. **Refresh Access Token**
`POST /user/token/refresh/`

- Automatically uses `refresh_token` from cookies

#### Response:
- `200 OK`
```json
{
  "message": "Access token refreshed"
}
```

> 🔁 New access token is sent as a cookie. Refresh token remains the same.

---

### 5. **Logout User**
`POST /user/logout/`

- Clears the `refresh_token` cookie and blacklists the token.

#### Response:
- `200 OK`
```json
{
  "message": "Logout successful"
}
```

---

### 6. **Update User Profile**
`PATCH /user/update-profile/`

- Requires: `access_token` cookie
- Auth Required: ✅

#### Request Body (Any subset of these fields):
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "phone_number": "0123456789",
  "photoURL": "https://example.com/image.jpg",
  "bio": "This is a test bio"
}
```

#### Response:
- `200 OK`
```json
{
  "message": "Profile updated successfully",
  "data": {
    "first_name": "Updated",
    "last_name": "Name",
    "phone_number": "0123456789",
    "photoURL": "https://example.com/image.jpg",
    "bio": "This is a test bio"
  }
}
```

---

### 7. **Change Password**
`PATCH /user/change-password/`

- Requires: `access_token` cookie

#### Request Body:
```json
{
  "old_password": "oldpassword123",
  "new_password": "newsecurepassword456"
}
```

#### Response:
- `200 OK`
```json
{
  "message": "Password updated successfully."
}
```

---

## 🔐 Authentication Overview

| Action              | Endpoint                  | Method | Auth Required | Description                                     |
|---------------------|---------------------------|--------|----------------|-------------------------------------------------|
| Register            | `/user/register/`         | POST   | ❌             | Create a new user                               |
| Login               | `/user/token/`            | POST   | ❌             | Authenticates and sets access/refresh cookies   |
| Profile (Get)       | `/user/`                  | GET    | ✅             | Get logged-in user's info                       |
| Refresh Token       | `/user/token/refresh/`    | POST   | ⛔             | Requires refresh token cookie                   |
| Logout              | `/user/logout/`           | POST   | ❌             | Blacklists refresh token, clears cookies        |
| Update Profile      | `/user/update-profile/`   | PATCH  | ✅             | Update user details                             |
| Change Password     | `/user/change-password/`  | PATCH  | ✅             | Update user's password                          |

---

## 🍪 Cookie Strategy

- `access_token` (15 min expiry)  
- `refresh_token` (7 day expiry)  
- Both cookies are:
  - HTTP-only
  - `SameSite=Lax`
  - `Secure=True` in production
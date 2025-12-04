# API Documentation

## Authentication & User Management

Base URL: `/api/accounts`

### 1. User Registration
**Endpoint:** `POST /register/`
**Access:** Public
**Description:** Register a new user account.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "StrongPassword123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "status": "success",
    "message": "User registered successfully",
    "data": {
        "id": "uuid-string",
        "email": "user@example.com",
        "full_name": "John Doe"
    }
}
```

### 2. Login
**Endpoint:** `POST /token/`
**Access:** Public
**Description:** Authenticate user and receive JWT tokens (set in cookies).

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "StrongPassword123!"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "id": "uuid-string",
        "email": "user@example.com",
        "full_name": "John Doe",
        "is_verified": false
    }
}
```
*Note: `access_token` and `refresh_token` are set as HttpOnly cookies.*

### 3. Logout
**Endpoint:** `POST /token/revoke/`
**Access:** Authenticated
**Description:** Logout user and clear authentication cookies.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Logout successful"
}
```

### 4. Refresh Token
**Endpoint:** `POST /token/refresh/`
**Access:** Public (Requires `refresh_token` cookie)
**Description:** Refresh access token using the refresh token cookie.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Token refreshed successfully"
}
```

### 5. Get User Profile
**Endpoint:** `GET /me/`
**Access:** Authenticated
**Description:** Retrieve current user's profile information.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Profile retrieved successfully",
    "data": {
        "id": "uuid-string",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone": null,
        "photoURL": "...",
        "bio": null,
        "date_of_birth": null,
        "is_verified": false,
        "is_email_verified": false,
        "is_phone_verified": false,
        "active_role": null,
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
}
```

### 6. Update User Profile
**Endpoint:** `PATCH /me/`
**Access:** Authenticated
**Description:** Update user profile details.

**Request Body:**
```json
{
    "first_name": "Johnny",
    "last_name": "Doe",
    "phone": "+1234567890",
    "bio": "Food lover",
    "date_of_birth": "1990-01-01",
    "photoURL": "https://example.com/photo.jpg"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Profile updated successfully",
    "data": { ... }
}
```

### 7. Change Password
**Endpoint:** `PATCH /me/password/`
**Access:** Authenticated
**Description:** Change user password.

**Request Body:**
```json
{
    "old_password": "OldPassword123!",
    "new_password": "NewStrongPassword123!"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Password changed successfully"
}
```

### 8. Password Reset Request
**Endpoint:** `POST /password-reset/`
**Access:** Public
**Description:** Request a password reset link via email.

**Request Body:**
```json
{
    "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "If an account exists with this email, a password reset link has been sent."
}
```

### 9. Password Reset Confirm
**Endpoint:** `POST /password-reset/confirm/`
**Access:** Public
**Description:** Reset password using the token received in email.

**Request Body:**
```json
{
    "token": "reset-token",
    "uidb64": "encoded-uid",
    "new_password": "NewStrongPassword123!"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Password has been reset successfully."
}
```

### 10. Request Email Verification
**Endpoint:** `POST /verify-email/request/`
**Access:** Authenticated
**Description:** Request a new email verification link.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Verification email sent successfully"
}
```

### 11. Confirm Email Verification
**Endpoint:** `POST /verify-email/confirm/`
**Access:** Public
**Description:** Verify email using the token.

**Request Body:**
```json
{
    "token": "verification-token"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Email verified successfully"
}
```

### 12. Request Phone Verification
**Endpoint:** `POST /verify-phone/request/`
**Access:** Authenticated
**Description:** Request an OTP for phone verification.

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Verification OTP sent successfully"
}
```

### 13. Confirm Phone Verification
**Endpoint:** `POST /verify-phone/confirm/`
**Access:** Authenticated
**Description:** Verify phone number using OTP.

**Request Body:**
```json
{
    "otp": "123456"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Phone verified successfully"
}
```

---

## Restaurant & Menu Management

Base URL: `/api/v1/restaurants`

### 1. Restaurants
**Endpoint:** `/restaurants/`

#### Get Restaurants
**Method:** `GET`
**Access:** Public (Approved & Active only), Staff (All)
**Query Parameters:**
- `search`: Search by name, description, city, or street address.
- `ordering`: Sort by `name` or `created_at`.
- `is_active`: Filter by active status (Staff only).
- `is_approved`: Filter by approval status (Staff only).

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Pizza Palace",
            "description": "Best Pizza in town",
            "logo": "http://example.com/logo.jpg",
            "is_approved": true,
            "is_active": true
        }
    ]
}
```

#### Create Restaurant
**Method:** `POST`
**Access:** Authenticated (Owner)
**Body:**
```json
{
    "name": "New Restaurant",
    "phone": "1234567890",
    "email": "contact@restaurant.com",
    "description": "Description"
}
```

#### Approve Restaurant
**Endpoint:** `/restaurants/{id}/approve/`
**Method:** `POST`
**Access:** Admin
**Body:**
```json
{
    "is_approved": true,
    "is_active": true
}
```

### 2. Branches
**Endpoint:** `/branches/`

#### Get Branches
**Method:** `GET`
**Access:** Public
**Query Parameters:**
- `search`: Search by name, restaurant name, or city.
- `branch_type`: Filter by type (`DINE_IN`, `DELIVERY`, `PICKUP`).
- `restaurant`: Filter by restaurant ID.

### 3. Menu Items
**Endpoint:** `/menu-items/`

#### Get Menu Items
**Method:** `GET`
**Access:** Public
**Query Parameters:**
- `search`: Search by name, description, or category name.
- `ordering`: Sort by `price` or `name`.
- `category`: Filter by category ID.
- `cuisine`: Filter by cuisine ID.
- `is_vegetarian`: `true`/`false`
- `is_vegan`: `true`/`false`
- `is_gluten_free`: `true`/`false`
- `is_available`: `true`/`false`

**Response (200 OK):**
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "name": "Veggie Pizza",
            "price": "15.00",
            "ingredients": "Cheese, Tomato",
            "allergens": "Dairy",
            "is_vegetarian": true
        }
    ]
}
```

### 4. Categories
**Endpoint:** `/categories/`
**Method:** `GET`
**Access:** Public
**Description:** List all food categories.

---

## Cart Management

Base URL: `/api/v1/cart`

### 1. Get Cart
**Endpoint:** `/`
**Method:** `GET`
**Access:** Authenticated
**Description:** Retrieve the current user's cart. Creates one if it doesn't exist.

**Response (200 OK):**
```json
{
    "id": 1,
    "total_price": 30.00,
    "items": [
        {
            "id": 1,
            "menu_item": 5,
            "menu_item_name": "Burger",
            "quantity": 2,
            "subtotal": 30.00
        }
    ]
}
```

### 2. Add Item to Cart
**Endpoint:** `/add/`
**Method:** `POST`
**Access:** Authenticated
**Body:**
```json
{
    "menu_item": 5,
    "quantity": 1
}
```

### 3. Update Item Quantity
**Endpoint:** `/items/{id}/`
**Method:** `PATCH`
**Access:** Authenticated
**Body:**
```json
{
    "quantity": 3
}
```

### 4. Remove Item
**Endpoint:** `/items/{id}/`
**Method:** `DELETE`
**Access:** Authenticated

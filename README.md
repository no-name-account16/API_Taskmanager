Ministry of Justice Task manager Project


# Task Manager API Documentation


## Quick Start

### Prerequisites
- Python 3.10+
- pip
- SQLite (included with Python)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
# Run the application
# from the root directory type .\run.bat
# or
# cd backend
python -m uvicorn main:app --reload
follow the onscreen infomation
```

### Access Documentation
Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Document In PDF format is in directory

## API Endpoints

### Base URL
```
http://localhost:8000
```

---

## Authentication

### Register a New User
**POST** `/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "john_smith",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_smith",
  "created_at": "2024-01-23T10:30:00"
}
```

**Errors:**
- `400 Bad Request`: Username already exists

---

### Login
**POST** `/token`

Authenticate and receive an access token.

**Request Body (Form Data):**
```
username: john_smith
password: password123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage:**
Include the token in subsequent requests:
```
Authorization: Bearer <your_access_token>
```

**Errors:**
- `401 Unauthorized`: Invalid credentials

---

### Get Current User
**GET** `/users/me`

Retrieve information about the authenticated user.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_smith",
  "created_at": "2024-01-23T10:30:00"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or missing token

---

## Tasks

All task endpoints require authentication.

### Get All Tasks
**GET** `/tasks`

Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "status": "in_progress",
    "due_date": "2024-01-25T17:00:00",
    "user_id": 1,
    "created_at": "2024-01-23T10:30:00"
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "description": null,
    "status": "pending",
    "due_date": "2024-01-24T12:00:00",
    "user_id": 1,
    "created_at": "2024-01-23T11:00:00"
  }
]
```

---

### Create a Task
**POST** `/tasks`

Create a new task.

**Headers:**
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "pending",
  "due_date": "2024-01-25T17:00:00"
}
```

**Field Descriptions:**
- `title` (required): Task title, max 200 characters
- `description` (optional): Detailed description
- `status` (required): One of "pending", "in_progress", "completed"
- `due_date` (required): ISO format datetime, must be in the future

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "pending",
  "due_date": "2024-01-25T17:00:00",
  "user_id": 1,
  "created_at": "2024-01-23T10:30:00"
}
```

**Errors:**
- `400 Bad Request`: Invalid data or due date in the past
- `401 Unauthorized`: Invalid or missing token

---

### Get a Specific Task
**GET** `/tasks/{task_id}`

Retrieve details of a specific task.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Parameters:**
- `task_id` (path): The ID of the task

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "in_progress",
  "due_date": "2024-01-25T17:00:00",
  "user_id": 1,
  "created_at": "2024-01-23T10:30:00"
}
```

**Errors:**
- `404 Not Found`: Task not found or doesn't belong to user
- `401 Unauthorized`: Invalid or missing token

---

### Update Task Status
**PATCH** `/tasks/{task_id}/status`

Update the status of a task.

**Headers:**
```
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

**Parameters:**
- `task_id` (path): The ID of the task

**Request Body:**
```json
{
  "status": "completed"
}
```

**Valid Status Values:**
- `pending`
- `in_progress`
- `completed`

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "completed",
  "due_date": "2024-01-25T17:00:00",
  "user_id": 1,
  "created_at": "2024-01-23T10:30:00"
}
```

**Errors:**
- `400 Bad Request`: Invalid status value
- `404 Not Found`: Task not found or doesn't belong to user
- `401 Unauthorized`: Invalid or missing token

---

### Delete a Task
**DELETE** `/tasks/{task_id}`

Delete a task permanently.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Parameters:**
- `task_id` (path): The ID of the task

**Response (204 No Content)**

**Errors:**
- `404 Not Found`: Task not found or doesn't belong to user
- `401 Unauthorized`: Invalid or missing token

---

##  Authentication Flow

1. **Register** a new user account (`POST /register`)
2. **Login** to receive an access token (`POST /token`)
3. **Use the token** in the Authorization header for all protected endpoints
4. Token expires after **30 minutes**
5. **Re-login** when token expires

### Example Authentication Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'

# 2. Login
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=pass123"

# Response: {"access_token":"eyJ...","token_type":"bearer"}

# 3. Use token for requests
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer eyJ..."
```

---

##  Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid data or request |
| 401 | Unauthorized - Invalid or missing authentication |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

##  Testing 

### Register and Login using powershell 
```bash
# Register
$body = @{
    username = "testpaul"
    email = "testpaul@example.com"
    password = "password"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/register"  \
                       -Method Post -ContentType "application/json" -Body $body


Result: 
        username email                id
        -------- -----                --
        testpaul testpaul@example.com  7

--------------------------------------------------------

Login

$loginBody = "grant_type=password&username=testpaul&password=password"
$response = Invoke-RestMethod -Uri "http://localhost:8000/login" `
    -Method Post `
    -ContentType "application/x-www-form-urlencoded" `
    -Body $loginBody

$TOKEN = $response.access_token
Write-Host "Logged in successfully!" -ForegroundColor Green
Write-Host "Token: $TOKEN`n" -ForegroundColor Cyan

Result:
Logged in successfully!
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0cGF1bCIsImV4cCI6MTc3MDEwOTI4N30.xrNsRk0Y03biQNOVpBDKd5XkKXQKoc1Iyn-JUgb4Ttw

Get all tasks
$tasks = Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
    -Method Get `
    -Headers @{ Authorization = "Bearer $TOKEN" }

Write-Host "Retrieved $($tasks.Count) tasks" -ForegroundColor Green
$tasks | Format-Table

Result:

title                    description     status  due_date            id user_id
-----                    -----------     ------  --------            -- -------
New Task from PowerShell Created via API pending 2024-12-31T23:59:59  7       7

------------------------------------------------------------------------------------
Create a task
$taskBody = @{
    title = "New Task from PowerShell"
    description = "Created via API"
    status = "pending"
    due_date = "2024-12-31T23:59:59"
} | ConvertTo-Json

$newTask = Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
    -Method Post `
    -Headers @{ Authorization = "Bearer $TOKEN" } `
    -ContentType "application/json" `
    -Body $taskBody

Write-Host "Task created with ID: $($newTask.id)" -ForegroundColor Green

Result:
Task created with ID: 7

```

##  Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Invalid Credentials:**
```json
{
  "detail": "Incorrect username or password"
}
```

**Task Not Found:**
```json
{
  "detail": "Task not found"
}
```

**Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "due_date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

##  Data Models

### User
```typescript
{
  id: number;
  username: string;
  created_at: datetime;
}
```

### Task
```typescript
{
  id: number;
  title: string;          // max 200 chars
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  due_date: datetime;    
  user_id: number;
  created_at: datetime;
}
```

---

##  Security Notes

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- Each user can only access their own tasks
- CORS is enabled for development
- Use HTTPS in production environments

---


## Requirements

see Requirements.txt
```



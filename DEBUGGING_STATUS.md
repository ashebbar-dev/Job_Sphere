# Debugging Status - 422 Errors

## Problem
All endpoints with `@jwt_required()` are returning 422 (Unprocessable Entity) errors:
- GET /api/tpo/companies
- GET /api/tpo/drives
- POST /api/tpo/companies
- GET /api/student/drives/available
- GET /api/hod/students/pending
- GET /api/hod/stats

## What Works
- Registration (POST /api/auth/register) - ✅ 201 responses
- Login (POST /api/auth/login) - ✅ 200 responses
- Database connection is working
- Database tables exist (users, students, hods, tpos, etc.)

## Debugging Steps Completed

### 1. Added Error Handling to Routes (backend/routes/tpo.py)
```python
@tpo_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    try:
        companies = Company.query.all()
        return jsonify([...]), 200
    except Exception as e:
        print(f"Error getting companies: {str(e)}")
        return jsonify({'error': str(e)}), 500
```
**Result:** No error messages appeared (route not being reached)

### 2. Added Error Handling to Decorator (backend/utils/decorators.py)
```python
def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
                ...
            except Exception as e:
                print(f"Error in role_required decorator: {str(e)}")
                return jsonify({'error': f'Authorization error: {str(e)}'}), 500
```
**Result:** No error messages appeared

### 3. Added Global Error Handlers (backend/app.py)
```python
@app.errorhandler(422)
def handle_unprocessable_entity(e):
    print(f"422 ERROR CAUGHT: {str(e)}")
    ...

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"GENERAL EXCEPTION CAUGHT: {type(e).__name__}: {str(e)}")
    ...
```
**Result:** Error handlers not triggered (422 not being raised as exception)

### 4. Added Request/Response Logging (backend/app.py) - CURRENT STATE
```python
@app.before_request
def log_request_info():
    print(f"\n=== INCOMING REQUEST ===")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Headers: {dict(request.headers)}")

@app.after_request
def log_response_info(response):
    print(f"\n=== OUTGOING RESPONSE ===")
    print(f"Status: {response.status}")
    print(f"Path: {request.path}")
    if response.status_code == 422:
        print(f"422 RESPONSE DATA: {response.get_data(as_text=True)}")
    return response
```

## Next Steps - USER ACTION REQUIRED

**The backend has been reloaded with comprehensive logging. To diagnose the issue, please:**

1. **Open http://localhost:3000 in your browser**
2. **Login as TPO** (tpo@test.com / password123)
3. **Try to create a company** or just wait for the page to load
4. **Check the backend console** (where python app.py is running)

You should now see detailed logs like:
```
=== INCOMING REQUEST ===
Method: GET
Path: /api/tpo/companies
Headers: {...}

=== OUTGOING RESPONSE ===
Status: 422
Path: /api/tpo/companies
422 RESPONSE DATA: <actual error message>
```

## Hypothesis

The 422 error is likely being returned directly by Flask-JWT-Extended or Flask-SQLAlchemy at a level that bypasses normal error handling. Possible causes:

1. **JWT Token Format Issue** - Token might be malformed or in wrong format
2. **Database Session Issue** - SQLAlchemy session management problem
3. **CORS or Content-Type Issue** - Request headers might be incorrect
4. **Flask-JWT Configuration** - JWT extension might be misconfigured

The request/response logging will reveal:
- If the request is reaching Flask at all
- What headers are being sent (especially Authorization header)
- What the actual 422 response body contains

## Files Modified During Debugging

1. `backend/routes/tpo.py` - Added try-catch to get_companies(), get_drives(), create_company()
2. `backend/utils/decorators.py` - Added try-catch to role_required decorator
3. `backend/app.py` - Added global error handlers and request/response logging

All changes are non-breaking and only add logging/error handling.

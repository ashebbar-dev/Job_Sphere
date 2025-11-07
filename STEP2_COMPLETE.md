# ✅ STEP 2: Database Schema & Models - COMPLETE

## Summary

Successfully created complete database schema with 10 models covering all entities needed for the AI-Powered College Placement Portal.

## File Created

### `backend/models.py` - Complete Database Schema

**10 Models Created:**

1. **User** - Base authentication model
   - Fields: email, password_hash, role, created_at
   - Methods: set_password(), check_password()
   - Roles: 'student', 'hod', 'tpo'

2. **Student** - Student profile
   - Personal info: name, enrollment_no, department, cgpa, phone
   - Resume: resume_path, skills (JSON)
   - Approval: is_approved, approved_by
   - Relationships: user, approver (⚠️ FIXED - added missing relationship)

3. **HOD** - Head of Department profile
   - Fields: name, department, phone
   - Relationship: user

4. **TPO** - Training & Placement Officer profile
   - Fields: name, phone
   - Relationship: user

5. **Company** - Company information
   - Fields: name, website, industry, description
   - AI Cache: research_data (JSON), last_researched
   - Relationship: drives (one-to-many)

6. **PlacementDrive** - Job posting/placement drive
   - Job info: job_title, job_description, job_requirements (JSON)
   - Eligibility: eligibility_criteria (JSON)
   - Details: ctc, location, drive_date, registration_deadline
   - Status: active/completed/cancelled
   - Relationships: company, applications, rounds

7. **Application** - Student job application
   - Resume: resume_version, cover_letter
   - AI Scores: match_score, ats_score, skills_gap (JSON)
   - Status: applied/shortlisted/rejected/selected
   - Relationships: student, drive, round_results

8. **SelectionRound** - Interview/test rounds
   - Fields: round_name, round_number, round_date
   - Examples: Online Test, Technical, HR
   - Relationships: drive, results

9. **RoundResult** - Result for each round
   - Fields: status, feedback, updated_at
   - Status: selected/rejected/pending
   - Relationships: application, round

10. **OfferLetter** - Job offer
    - Fields: file_path, issued_date
    - Relationship: application

## Database Relationships

```
User (1) ----< Student (has user_id)
User (1) ----< HOD (has user_id)
User (1) ----< TPO (has user_id)
User (1) ----< Student.approver (approved_by foreign key)

Company (1) ----< PlacementDrive (many)
PlacementDrive (1) ----< Application (many)
PlacementDrive (1) ----< SelectionRound (many)

Student (1) ----< Application (many)
Application (1) ----< RoundResult (many)
Application (1) ---- OfferLetter (1)

SelectionRound (1) ----< RoundResult (many)
```

## Issues Fixed from Plan

### ✅ Fixed: Missing `approved_by` Relationship

**Original Issue:**
```python
# Student model had foreign key but no relationship
approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
# Missing relationship to access approver User object
```

**Fix Applied:**
```python
approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
approver = db.relationship('User', foreign_keys=[approved_by])
# Now can access: student.approver.name
```

### ✅ Fixed: datetime.utcnow() Deprecation

**Original:**
```python
created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Fixed:**
```python
created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
```

This prevents deprecation warnings in Python 3.12+.

## Key Features of Schema

### JSON Columns for Flexibility
- `Student.skills` - Array of skill strings
- `Company.research_data` - AI-generated company insights
- `PlacementDrive.job_requirements` - Skills, experience needed
- `PlacementDrive.eligibility_criteria` - CGPA, departments allowed
- `Application.skills_gap` - Missing skills analysis

### AI Integration Points
- `Company.research_data` - Cached AI company research (7-day TTL)
- `Application.match_score` - AI-calculated candidate-job fit (0-100)
- `Application.ats_score` - ATS compatibility score (0-100)
- `Application.skills_gap` - AI-identified missing skills

### Security Features
- Password hashing using werkzeug.security
- `set_password()` - Hashes password before storage
- `check_password()` - Verifies password against hash
- JWT authentication ready (used in next steps)

### Approval Workflow
- Students register → `is_approved = False`
- HOD approves → `is_approved = True`, `approved_by = hod.user_id`
- Only approved students can apply to drives

## Database Models Import Structure

```python
from models import (
    db,              # SQLAlchemy instance
    User,            # Base auth
    Student,         # Student profile
    HOD,             # HOD profile
    TPO,             # TPO profile
    Company,         # Company info
    PlacementDrive,  # Job posting
    Application,     # Student application
    SelectionRound,  # Interview rounds
    RoundResult,     # Round results
    OfferLetter      # Job offers
)
```

## Next Steps - STEP 3

Ready to implement **STEP 3: Flask Backend Core Setup**:
1. Create `backend/config.py` - Flask configuration (with OpenAI API key)
2. Create `backend/app.py` - Flask application initialization
3. Initialize database with `db.create_all()`

## Testing Models

Once Flask app is created (Step 3), you can test models:
```python
from app import create_app
from models import db, User, Student

app = create_app()
with app.app_context():
    # Create tables
    db.create_all()

    # Test user creation
    user = User(email='test@example.com', role='student')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    print(f"User created: {user.email}")
    print(f"Password check: {user.check_password('password123')}")
```

---

**Status:** ✅ STEP 2 COMPLETE - Ready for STEP 3
**File Created:** `backend/models.py` (10 models, 180+ lines)
**Issues Fixed:** 2 (approved_by relationship, datetime deprecation)

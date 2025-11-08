# ⚡ QUICK START - IMPORTANT!

## 🚨 **CRITICAL: You Must Register Before Login!**

The database is fresh and has NO users yet. Follow these steps:

### **Step 1: Go to Register Page**
1. Open: `http://localhost:3000`
2. Click "Register" at the bottom of the login page

### **Step 2: Create TPO Account (Do this FIRST)**
```
Role: TPO
Email: tpo@test.com
Password: password123
Name: Test TPO
Phone: 1234567890
```
Click "Register" → Wait for success message → Go back to login

### **Step 3: Create Student Account**
```
Role: Student
Email: student@test.com
Password: password123
Name: Test Student
Enrollment No: STU001
Department: CSE (Computer Science)
CGPA: 8.5
Phone: 1234567890
```
Click "Register" → Wait for success message → Go back to login

### **Step 4: Create HOD Account**
```
Role: HOD
Email: hod@test.com
Password: password123
Name: Test HOD
Department: CSE (Computer Science)
Phone: 1234567890
```
Click "Register" → Wait for success message → Go back to login

### **Step 5: Now You Can Login!**
Use any of the accounts you just created:
- `tpo@test.com` / `password123`
- `student@test.com` / `password123`
- `hod@test.com` / `password123`

---

## **Demo Flow After Registration:**

### **1. Login as TPO First**
- Create a company (e.g., "Google", "Tech Industry", "www.google.com")
- Create a placement drive:
  - Select the company
  - Job Title: "Software Engineer"
  - Job Description: "Full stack development role"
  - CTC: "15 LPA"
  - Location: "Bangalore"

### **2. Login as HOD**
- Approve the student (Test Student should appear in pending list)

### **3. Login as Student**
- Upload a resume (PDF file)
- View available drives
- Click "Analyze Fit with AI" on the drive
- See the AI magic! 🎨
- Apply to the job

---

## **Why This Happens:**
- Fresh database = no users
- Registration creates users in database
- Login checks if user exists
- That's why you got 401 errors!

---

**NOW TRY IT! 🚀**

# MFU Web Portal - User Guide

This guide provides instructions on how to use the MFU Web Portal for different user roles. The portal is designed to manage sports centers, athletes, events, and finances efficiently.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Accessing the Portal](#accessing-the-portal)
   - [Registration & Login](#registration--login)
2. [User Roles Overview](#user-roles-overview)
3. [Admin Portal](#admin-portal)
   - [Managing Users](#managing-users)
   - [Managing Centers](#managing-centers)
4. [Coach Portal](#coach-portal)
   - [Dashboard Overview](#coach-dashboard)
   - [Managing Teams](#managing-teams)
   - [Training Sessions](#training-sessions)
   - [Athlete Evaluation](#athlete-evaluation)
5. [Athlete Portal](#athlete-portal)
   - [My Profile](#my-profile)
   - [My Scores & Rankings](#my-scores--rankings)
   - [Events](#participating-in-events)
6. [Finance & Inventory Portal](#finance--inventory-portal)
   - [Equipment Management](#equipment-management)
   - [Financial Transactions](#financial-transactions)
7. [Events Management](#events-management)

---

## 1. Getting Started

### Accessing the Portal
The portal is accessible via your web browser. 
- **Production URL**: `https://yourdomain.com` (Example)
- **Local Development**: `http://127.0.0.1:8000`

### Registration & Login
1. **Sign Up**: Click **"Register"** on the homepage. Enter your email, password, and personal details. You can also sign up using your Google account.
2. **Login**: Click **"Login"** and enter your credentials.
3. **Role Assignment**: By default, new users may have limited access. An **Admin** must assign specific roles (Coach, Athlete, Staff) to your account.

---

## 2. User Roles Overview

Your dashboard and available features depend on your assigned role:

- **Admin**: Full system control. Manages users, roles, and centers.
- **Coach**: Manages teams, schedules training, and evaluates athletes.
- **Athlete**: Views updated scores, rankings, and upcoming events.
- **Parent**: (If applicable) Views progress and data for their linked child athletes.
- **Finance & Inventory Manager**: Handles payments, expenses, and equipment tracking.

---

## 3. Admin Portal

*Access: Users with `Admin` role.*

### Managing Users
1. Go to **Admin Dashboard**.
2. Click **Users** to view all registered accounts.
3. **Edit User**: Click a username to update details or assign Roles (e.g., promote a user to 'Coach').
4. **Deactivate**: You can deactivate users instead of deleting them to preserve history.

### Managing Centers
1. Navigate to **Centers**.
2. **Add Center**: details like Name, Address, and Facilities (Gym, Pool, Track).
3. **Assign Head**: You can link a `Center Head` user to a specific facility.

---

## 4. Coach Portal

*Access: Users with `Coach` role.*

### Coach Dashboard
Your central hub showing:
- **Upcoming Sessions**: Next scheduled training.
- **My Teams**: Teams you are assigned to.
- **Top Athletes**: Quick view of top-performing athletes.

### Managing Teams
1. Click **Teams** in the navigation.
2. View your active competition teams.
3. **Head Coaches** can create new teams and assign regular coaches.
4. Add **Athletes** to teams to track their group performance.

### Training Sessions
1. Go to **Training Sessions**.
2. **Create Session**: Click "Add Session", set the date, time, and center.
3. **Attendance**: Mark which athletes attended after the session.
4. **Filter**: Toggle between `Upcoming` and `Past` sessions.

### Athlete Evaluation
1. Go to **Athletes**.
2. Select an athlete profile.
3. **Add Score**: Record performance metrics (Time, Distance, or Points) for specific events.
4. **Certificates**: Issue evaluation certificates for achievements.

---

## 5. Athlete Portal

*Access: Users with `Athlete` role.*

### My Profile
- View your personal details, medical info (allergies/conditions), and emergency contacts.
- Keep this updated for your safety during training.

### My Scores & Rankings
- **Scores**: View history of your performance in various events.
- **Rankings**: See your current standing in your category (e.g., U-18).
- **Certificates**: Download digital certificates issued by your coaches.

### Participating in Events
1. Browse **Upcoming Events**.
2. Click **Register** for competitions or seminars.
3. Check your registration status (Pending/Confirmed).

---

## 6. Finance & Inventory Portal

*Access: Users with `Finance & Inventory Manager` role.*

### Equipment Management
1. Go to **Inventory**.
2. **Add Equipment**: Log new purchases (Name, Cost, Quantity).
3. **Track Status**: Update condition (`Good`, `Damaged`) and status (`Available`, `In Use`).
4. **Maintenance**: Schedule and track equipment repairs.

### Financial Transactions
1. Go to **Finances**.
2. **Record Transaction**: Log income (Fees, Grants) or expenses (Salaries, Maintenance).
3. **Reports**: View financial summaries by Center or Event.

---

## 7. Events Management

*Access: Admins and Organizers.*

1. **Create Event**: Set Name, Date, Type (Competition/Training), and Capacity.
2. **Manage Registrations**: View and approve participant sign-ups.
3. **Publish**: Switch event status from `Draft` to `Published` to make it visible to athletes.

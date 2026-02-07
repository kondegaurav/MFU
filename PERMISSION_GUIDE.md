# MFU Portal - Permission Management Guide

This document explains how to manage user permissions within the MFU Portal using the unique **Role** and **Role Tag** system.

> **Important:** Do NOT use the default Django "Groups" section. It is not connected to this application's permission logic.

## 1. Concepts

The system uses a two-layer approach to permissions:

1.  **Roles**: Define the primary portal Access (e.g., Coach Portal, Athlete Portal). Every user must have at least one Role.
2.  **Role Tags**: Grant *extra* privileges within that role (e.g., A Coach who can also create teams).

---

## 2. Managing Coach Permissions

### A. Assigning Basic Coach Access (Training Sessions)
To allow a user to log in as a Coach and schedule training sessions:

1.  Log in to the **Admin Portal**.
2.  Navigate to **Users** and click the user you want to update.
3.  Scroll down to the **User Roles** inline section.
4.  Click **Add another User Role**.
5.  Select **Coach** from the dropdown menu.
6.  Click **Save**.

*The user can now access the Coach Dashboard and add Training Sessions.*

### B. Granting "Head Coach" Status (Create Teams)
Only Head Coaches can create new Competition Teams. To upgrade a Coach:

1.  Navigate to **Users** and select the Coach.
2.  Scroll down to the **User Role Tags** inline section (usually below Roles).
3.  Click **Add another User Role Tag**.
4.  Select **Head Coach**.
5.  Click **Save**.

*The user now has permission to create and manage Competition Teams.*

### C. Managing Team Members
Currently, the most direct way to manage team rosters is via the Admin panel:

1.  Navigate to **Competition Teams**.
2.  Select the specific Team.
3.  Use the **Team Members** section to add or remove Athletes.

---

## 3. Managing Center Permissions

### Granting Center Head Access
To allow an Admin to manage events and volunteering opportunities for a center:

1.  Navigate to **Users** and select the Admin user.
2.  Ensure they have the **Admin** role in the **User Roles** section.
3.  In the **User Role Tags** section, add the **Center Head** tag.
4.  Click **Save**.

---

## 4. Summary Table

| Permission Needed | Required Role | Required Tag |
| :--- | :--- | :--- |
| Login to Coach Portal | Coach | *(None)* |
| create Training Sessions | Coach | *(None)* |
| Create Competition Teams | Coach | **Head Coach** |
| Manage Events | Admin | **Center Head** |
| Manage Equipment | Admin | **Center Head** |

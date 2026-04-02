# EHR Bridge API - User Guide for Clients

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Method 1: Using Swagger Documentation](#method-1-using-swagger-documentation)
3. [Method 2: Using Postman Collection](#method-2-using-postman-collection)
4. [API Examples](#api-examples)
5. [Troubleshooting](#troubleshooting)

---

## Getting Started

### What You Need
- **Production Server URL**: `http://44.222.254.215:8001`
- **Your Login Credentials**: Email and password provided by your administrator
- **Connection ID**: Your EHR connection UUID (provided by your administrator)

### Important Information
- All APIs require authentication using a token
- You must login first to get your authentication token
- Each API request needs your **Connection ID** to identify which EHR system to use

---

## Method 1: Using Swagger Documentation

Swagger is a web-based tool that lets you test APIs directly in your browser.

### Step 1: Access Swagger Documentation
1. Open your web browser
2. Go to: `http://44.222.254.215:8001/api/docs/`
3. You will see a list of all available APIs

### Step 2: Login to Get Your Token
1. Find the **"Login API"** section (usually under "Authentication" or "Auth")
2. Click on **"POST /api/auth/login/"** to expand it
3. Click the **"Try it out"** button
4. In the **Request body**, enter:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
5. Click **"Execute"**
6. Copy the **"token"** value from the response (you'll need this for all other APIs)

### Step 3: Authorize Your Session
1. Look for the **"Authorize"** button at the top right of the Swagger page
2. Click it
3. In the **"Value"** field, enter: `token YOUR_TOKEN_HERE` (replace YOUR_TOKEN_HERE with the token you copied)
4. Click **"Authorize"** then **"Close"**

### Step 4: Test Any API
1. Find the API you want to test (e.g., "Patient Search")
2. Click on it to expand
3. Click **"Try it out"**
4. Fill in the required fields (see examples below)
5. Click **"Execute"**
6. View the response below

---

## Method 2: Using Postman Collection

Postman is a desktop application for testing APIs. It's more powerful than Swagger and allows you to save your requests.

### Step 1: Install Postman
1. Download Postman from: https://www.postman.com/downloads/
2. Install and open Postman

### Step 2: Import the Collection
1. In Postman, click **"Import"** button (top left)
2. Select the **"EHR_Bridge API Documentation.postman_collection.json"** file provided to you
3. The collection will appear in the left sidebar

### Step 3: Login First
1. In the collection, find and click **"Login API"**
2. Update the email and password in the **Body** section:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
3. Click **"Send"**
4. The token will be automatically saved for other requests

### Step 4: Update Your Connection ID
1. Open any API request in the collection
2. In the **Body** section, find the **"Source"** → **"ID"** field
3. Replace the connection ID with your own: `f1b377a2-6a55-4605-aaf0-49fb5edde26a`
4. This connection ID is used in all API requests

### Step 5: Test APIs
1. Click on any API request in the collection
2. Review and update the request body if needed
3. Click **"Send"**
4. View the response in the bottom panel

---

## API Examples

### 1. Patient Search API
**Purpose**: Search for patients by name

**Swagger Path**: `POST /api/patient/patient-search/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "PatientSearch",
    "EventType": "Query",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    }
  },
  "Patient": {
    "Demographics": {
      "FirstName": "John"
    }
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID
- Replace `"John"` with the first name you want to search for

**Response**: Returns a list of matching patients

---

### 2. Patient Query API (Get Patient Clinical Data)
**Purpose**: Get detailed clinical information for a specific patient

**Swagger Path**: `POST /api/patient/patient-query/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "Clinical Summary",
    "EventType": "PatientQuery",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    },
    "Events": [
      "Demographics"
    ]
  },
  "Patient": {
    "Identifiers": [
      {
        "ID": "PATIENT_ID_FROM_EHR",
        "IDType": "EHRID"
      }
    ]
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID
- Replace `PATIENT_ID_FROM_EHR` with the patient ID you got from Patient Search
- You can add more events like `"Allergies"`, `"Medications"`, `"Vitals"` if needed

**Response**: Returns patient clinical data based on the events you requested

---

### 3. Visit Query API
**Purpose**: Get visit/encounter information for a patient

**Swagger Path**: `POST /api/visit/visit-query/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "Visit",
    "EventType": "Query",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    }
  },
  "Patient": {
    "Identifiers": [
      {
        "ID": "PATIENT_ID_FROM_EHR",
        "IDType": "EHRID"
      }
    ]
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID
- Replace `PATIENT_ID_FROM_EHR` with the patient ID

**Response**: Returns visit/encounter information for the patient

---

### 4. Provider Query API
**Purpose**: Search for healthcare providers/practitioners

**Swagger Path**: `POST /api/provider/query/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "Provider",
    "EventType": "ProviderQuery",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    }
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID

**Response**: Returns a list of providers

---

### 5. Organization Query API
**Purpose**: Get organization information

**Swagger Path**: `POST /api/organization/organization-query/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "Organization",
    "EventType": "Query",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    }
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID

**Response**: Returns organization information

---

### 6. Document Reference Query API
**Purpose**: Get patient documents/clinical notes

**Swagger Path**: `POST /api/document-reference/query/`

**Minimal Request Body**:
```json
{
  "Meta": {
    "DataModel": "DocumentReference",
    "EventType": "Query",
    "Test": true,
    "Source": {
      "ID": "YOUR_CONNECTION_ID",
      "Name": "connectionid"
    }
  },
  "Patient": {
    "Identifiers": [
      {
        "ID": "PATIENT_ID_FROM_EHR"
      }
    ]
  }
}
```

**What to Change**:
- Replace `YOUR_CONNECTION_ID` with your connection UUID
- Replace `PATIENT_ID_FROM_EHR` with the patient ID

**Response**: Returns patient documents

---

## Troubleshooting

### Problem: "Unauthorized" or "401" Error
**Solution**:
- Make sure you've logged in and copied your token correctly
- In Swagger: Click "Authorize" and enter `token YOUR_TOKEN`
- In Postman: The token should be automatically saved after login

### Problem: "Connection not found" or "404" Error
**Solution**:
- Check that your Connection ID is correct
- Make sure you're using the right Connection ID for your EHR system

### Problem: "Bad Request" or "400" Error
**Solution**:
- Check that your JSON format is correct (no extra commas, proper quotes)
- Make sure all required fields are filled in
- Verify the patient ID exists in your EHR system

### Problem: Token Expired
**Solution**:
- Simply login again to get a new token
- Update the token in Swagger (Authorize button) or Postman (it should auto-update)

### Problem: Can't Find an API in Swagger
**Solution**:
- Make sure you're on the correct Swagger page: `http://44.222.254.215:8001/api/docs/`
- Use the search box at the top to find APIs by name
- Scroll through the list - APIs are organized by category

---

## Quick Reference

| API | Purpose | Required Fields |
|-----|---------|----------------|
| Patient Search | Find patients | Connection ID, First Name |
| Patient Query | Get patient data | Connection ID, Patient ID |
| Visit Query | Get visits | Connection ID, Patient ID |
| Provider Query | Get providers | Connection ID |
| Organization Query | Get organization | Connection ID |
| Document Query | Get documents | Connection ID, Patient ID |

---

## Need Help?

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Verify your Connection ID is correct
3. Make sure you're using the latest token from login
4. Contact your system administrator

---

**Last Updated**: 4/03/2026
**Version**: 1.0

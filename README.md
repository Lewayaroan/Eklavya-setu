# Eklavya Setu (एकलव्य सेतु)
### Unified Mobile Scholarship Portal & JAGO AI Voice Assistant for Tribal Students
**Smart India Hackathon 2026** | **Problem Statement ID: SIH26238**  
**Ministry:** Ministry of Tribal Affairs (MoTA) | **Theme:** Smart Automation / Software

---

## 📌 Executive Summary
The Ministry of Tribal Affairs (MoTA) administers five central scholarship schemes for Scheduled Tribe (ST) students across three disconnected platforms:
1. **National Scholarship Portal (NSP)** (Pre-Matric, Post-Matric, Top Class)
2. **Scholarship Fellowship Management Portal (SFMP - Canara Bank)** (National Fellowship / NFST)
3. **Standalone NOS Portal** (National Overseas Scholarship)

This fragmentation creates severe hurdles for tribal families: repetitive physical document verification, no single view of funds or status, risks of accidental dual-claims, and zero visibility into left-out students.

**Eklavya Setu** unifies all 5 MoTA schemes into a single, mobile-first interface powered by **APAAR ID (One Nation, One Student ID)**, **DigiLocker paperless verification**, and the **JAGO Multilingual Voice Assistant (Digital India Bhashini)**.

---

## 🌟 The 5 MoTA Schemes Unified in 1 App

| Scheme | Target Beneficiary | Key Benefit | Former Portal |
| :--- | :--- | :--- | :--- |
| **Pre-Matric ST** | Class 9 & 10 Day-Scholars/Hostellers | ₹3,500/year aid for school retention | NSP |
| **Post-Matric ST** | Class 11 to Post-Graduation | 100% Tuition Fees + Monthly Maintenance | NSP / State |
| **Top Class Education** | Premier Institutes (IITs, IIMs, NITs, AIIMS) | Full tuition + ₹86,000 living & laptop grant | NSP |
| **National Fellowship (NFST)** | M.Phil & Ph.D. Scholars | ₹37,000/month JRF stipend | Canara Bank SFMP |
| **National Overseas (NOS)** | Masters & Ph.D. in Top 500 Global Unis | 100% tuition + USD/GBP stipend | NOS Standalone Portal |

---

## 🚀 Key Innovations & Features

### 1. Unified 4-Step Application Tracker
Live API sync with NSP and PFMS servers providing end-to-end visibility:
$$\text{DigiLocker Verification} \longrightarrow \text{College Nodal Review} \longrightarrow \text{State Welfare Sanction} \longrightarrow \text{PFMS DBT Bank Credit}$$

### 2. JAGO Conversational Voice AI (Bhashini-Integrated)
* Enables tribal students to query status and resolve deficiencies by speaking in their mother tongue (**Hindi**, **English**, **Santhali / ᱥᱟᱱᱛᱟᱲᱤ**, **Telugu / తెలుగు**, etc.).
* Reads out answers with text-to-speech audio synthesis directly in the browser.

### 3. Instant DigiLocker & APAAR Verification
* Cryptographically checks **Caste (ST/PVTG)** and **Income Certificates** directly via state revenue APIs without manual paper submissions.
* **Soft Mismatch Exception Resolver:** Name or spelling variations between Aadhaar and academic records are routed to institute teachers for a 1-click review rather than auto-rejecting the student.

### 4. Single-Avail & De-Duplication Guard
* Enforces the government's single-scholarship mandate across all 3 backend portals.
* Intercepts overlapping applications and provides automated transfer/upgrade workflows without disqualifying the student.

### 5. Zero-Dropout Discovery Radar (MoTA Admin Intelligence)
* Calculates unreached tribal students at the district/block level:
  $$\text{Unreached ST Pool} = \text{UDISE+ Enrolled ST Students} - \text{Active Scholarship Beneficiaries}$$
* Flags high-PVTG zones with low uptake (e.g., Khunti, Mayurbhanj, Bastar) so District Welfare Officers can dispatch mobile biometric enrollment camps.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, Tailwind CSS, FontAwesome 6, Plus Jakarta Sans
* **Voice & Language:** Web Speech API, Digital India Bhashini ASR/TTS Engine
* **Interoperability:** DigiLocker API, APAAR / AISHE / UDISE+ Registry, PFMS DBT Webhooks
* **Deployment:** Mobile-first responsive Progressive Web App (PWA), zero external build dependencies

---

## 💻 Quick Start & Local Preview

Simply clone the repository and open `index.html` in any modern web browser:

```bash
git clone https://github.com/Lewayaroan/Eklavya-setu.git
cd Eklavya-setu
# Open directly in browser
start index.html
```

Or deploy to **Vercel** with one click:
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Lewayaroan/Eklavya-setu)

---

## 📜 License
MIT License • Created for Smart India Hackathon (SIH 2026)

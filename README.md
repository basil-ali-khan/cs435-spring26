# CS 435 – Spring 2026

This repository is the shared course workspace for **CS 435** practical assignments on **Privacy Enhancing Technologies (PETs)**, **Secure AI**, and related implementation demos.

For **Lecture 8**, each group is assigned one technique to study, implement in Python, and connect to a real cloud-native offering from **AWS**, **GCP**, or **Azure**.

---

## Lecture 8 Assignment Goals

Each group should:

1. **Understand the assigned technique** and what problem it solves.
2. **Build a small practical example in Python**.
3. Show the work as either a:
   - **Jupyter notebook** (`.ipynb`), or
   - **standalone Python app** (`.py`)
4. Identify **one native hyperscaler offering** that does similar work in practice.
5. Open a **pull request** to submit the work.
6. Be prepared to **discuss the implementation in class**.

> Use **dummy, synthetic, or public sample data only**. Do not upload real personal, financial, medical, or confidential data.

---

## Repository Structure

The Lecture 8 assignment folders are organized as follows:

- `Assignment_0_Tokenization_and_Masking/`
- `Assignment_1_Federated_Learning/`
- `Assignment_2_Differential_Privacy/`
- `Assignment_3_Secure_Multiparty_Computation/`
- `Assignment_4_Homomorphic_Encryption/`
- `Assignment_5_Trusted_Execution_Environment/`
- `Assignment_6_Secure_Aggregation/`
- `Assignment_7_Watermarking_and_Fingerprinting/`
- `Assignment_8_Adversarial_Robustness/`
- `Assignment_9_Access_Control_and_Data_Minimization/`
- `Assignment_10_Zero_Knowledge_Proofs/`

Each group should work **only inside its assigned folder**.

---

## What to Put in Your Assigned Folder

At minimum, each group folder should contain:

- Your **implementation** (`.ipynb` or `.py`)
- A folder-level `README.md` explaining:
  - group member names
  - the assigned technique
  - the scenario you implemented
  - how to run the code
  - expected output / result
  - one matching **AWS / GCP / Azure** service
- Any small supporting files needed to run the demo
- Optional screenshots, diagrams, or output samples

If your code needs extra libraries, include either:

- `requirements.txt`, or
- a short install section in your folder `README.md`

---

## Suggested Folder README Contents

Inside your assignment folder, your `README.md` should answer these questions clearly:

- Who is in the group?
- What technique were you assigned?
- What real-world problem does your demo solve?
- What files should the instructor run first?
- How do we install dependencies?
- What output should appear if the demo works?
- What is one native cloud counterpart for this technique?
- What tradeoff or lesson did your group learn?

---

## Submission Workflow

1. **Clone** the repository.
2. Create a **new branch** for your work.
3. Add your files to your assigned folder.
4. Update that folder’s `README.md`.
5. Commit your work with clear commit messages.
6. Open a **pull request** against the main repository.

### Suggested PR title format

`Lecture8 - Assignment X - Group Name`

Example:

`Lecture8 - Assignment 4 - Group Delta`

---

## Basic Local Setup

If you need a simple Python setup:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
pip install -U pip
```

Common libraries used across assignments may include:

```bash
pip install pandas numpy scikit-learn matplotlib jupyter phe cryptography
```

Install only what your assignment actually needs.

---

## Expectations for a Strong Submission

A strong submission should be:

- **practical** rather than abstract
- **small enough to run easily**
- **easy to understand**
- based on a **real scenario**
- connected to the lecture concepts
- explained clearly enough that your classmates can follow it

Your code does **not** need to be production-grade. It should show that your group understands the concept and can demonstrate it correctly.

---

## Cloud Counterpart Requirement

For each assignment, identify **one real cloud-native service** that performs similar work.

Examples:

- **Azure Confidential Computing / Confidential VMs** → Trusted Execution Environment concepts
- **AWS Clean Rooms** → privacy-preserving collaboration / restricted data sharing use cases
- **Google Cloud DLP** → tokenization, masking, and sensitive data transformation workflows

Do not just list the service name. Briefly explain:

- what it does
- why it matches your technique
- how it differs from your classroom implementation

---

## In-Class Discussion

These implementations will be discussed in class. Every group should be ready to explain:

- the technique in plain language
- the scenario you chose
- how your code works
- what result it produces
- what cloud service does similar work in practice
- one limitation, tradeoff, or design decision

---

## Academic Integrity and Safe Data Use

- Do your own group’s work.
- Give credit for any external libraries, examples, or references you use.
- Do not commit secrets, API keys, credentials, or large private datasets.
- Use synthetic or approved sample data only.

---

## Questions

Refer to the assignment handout for the full assignment details. If something is unclear, ask before the due date rather than guessing.

---

## Quick Reminder

- Work in your assigned folder
- Submit a PR
- Include runnable Python code
- Add a clear folder README
- Include one cloud counterpart
- Be ready to talk about it in class

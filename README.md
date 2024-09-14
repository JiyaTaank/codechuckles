The CodeChuckles is a web-based onlinejudge platform where users can practice coding by solving problems and submitting their solutions. The platform provides functionality to run code in various languages, evaluates the submissions against test cases, and maintains leaderboards based on the users' submissions.

Features:
User Authentication: Sign up, login, and manage user accounts using Django's built-in authentication system (User model and admin panel).
Question Management: List of programming problems categorized by difficulty, with search and filter options.
Code Execution: Supports running and submitting solutions in multiple programming languages (Python, C++ and C).
Leaderboards: Ranks users based on the number of correct solutions with the latest submission details.
Submissions: Tracks all attempts with statuses like Accepted, Rejected.
Profile Page: Displays user stats ( no. of attempted, accepted, rejected questions) and latest submissions detail for each attempted question.
Test Cases and Time Limits: Admin can add and manage test cases and set time limits for questions via the Django admin panel.

Tech Stack:
Backend: Django 4.2.2
Frontend: HTML, CSS, JavaScript
Containerization: Docker
Deployment: AWS EC2
Languages Supported: Python, C++, and C

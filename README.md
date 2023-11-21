<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Logo -->
<br />
<div align="center">
  <a href="https://github.com/mike-eziefule/Ezzy_Blog">
    <img src="./images/Ezzybank.png" alt="Logo" width="80%" height="20%">
  </a>
</div>

<br />

<div>
  <p align="center">
    <a href="https://github.com/mike-eziefule/Ezzy_Blog_api/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.loom.com/share/ed3cc4bfb8c743cd9371e2831a7785ec?sid=4be6af19-e752-4289-a180-bf065c0bd58a">View Demo</a>
    ·
    <a href="https://github.com/mike-eziefule/Ezzy_Blog/issues">Report Bug</a>
    ·
    <a href="https://github.com/mike-eziefule/Ezzy_Blog/issues">Request Feature</a>
  </p>
</div
---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-Ezzy-blog">About Ezzy Bank API</a>
      <ul>
        <li><a href="#user-module">User Module</a></li>
      </ul>
      <ul>
        <li><a href="#admin-module">Admin Module</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#lessons-learned">Lessons Learned</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Blog. -->
## About Ezzy Bank

Ezzy Bank is a cutting-edge fintech API, crafted with precision using FastAPI and Python. Empowering seamless financial transactions,
secure data handling, and rapid integration. Our API is designed to elivate your fintech solutions to new heights. Experiencing efficiency
and reliability at its core as you embark on a finincial journey of unparalleled financial innovation with our robust FASTAPI-powered platform.


### User module:

1. New users can register with Ezzy Bank by filling in some information:
    **upon registering, a new account number will be generated and added to your account
    **provided email address and password will be needed to login/authentication.
    **username and email will be unique hence, multiple accounts cannot have the same username and/or email.

2. Registered users can:
    -check balance, 
    -transfer to other account holder,
    -receive payment from other account holder
    -check transaction history,
    -block an account,
    -edit some profile information

3. Users can also make deposits or withdrawal by contacting the bank administrator (modelled here as over the counter staff)

4. All actions(transfer, withdrawal, login, checking account balance) performed by any user is captured in a LOG table and assigned a 
    unique 32digits number(UUID) which can be used to track any transaction dispute.

5.  When a account is blocked or inactive, any transfers or withdrawals made from that accout would br automatically reversed. and user is advised
    to contact the administrator


### Admin module:

1. The first account to sign up on the app is automatically stored as the administrator
2. Admin accounts can only be deleted by the software creator.
3. Admin reserves the right to edit all users information except the users login email and password
4. Admin user can perform the following actions:
    -deposit: funds are charged from admin account and credited to the user account
    -withdrawal: funds are charged from user account and credited to the administrator account
    -disable any user accounts: stop an account from transacting
    -enable any user accounts: allow an account transact
    -edit any user accounts: change user informations except account number, email and password
    -delete any user accounts except admin account.


5. All actions performed by the admin is captured in a LOG table and assigned a unique 32digits number(UUID) which can be used to track 
    any transaction dispute.

---

Ezzy Bank was built by <a href="https://github.com/mike-eziefule/" target="_blank">Eziefule Michael</a>, a Backend Engineering student at <a href="https://engineering.altschoolafrica.com/" target="_blank">AltSchool Africa</a> who's learning to create magic with the Python FastAPI framework.

A tutorial on how this project was built is available in [Michael_Ezzy's Space](https://hashnode.com/draft/6539339dbe20a1000f0b5edd) on Hashnode.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![FastAPI][fastapi]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project. -->
## Lessons Learned

Creating this blog helped me learn and practice:
* The use of python for backend development
* Debugging
* Routing
* Database Management
* Internet Security
* User Authentication
* User Authorization
* Documentation

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To get a local copy up and running, follow the steps below.

### Prerequisites

Python3: [Get Python](https://www.python.org/downloads/)

### Installation

1. Clone this repo
   ```sh
   git clone https://github.com/mike-eziefule/CRUD-bank-app.git
   ```
2. Activate the virtual environment(git bash on Windows)
   ```sh
   source virtual/Scripts/activate
   ```
3. Install project packages
   ```sh
   pip install -r requirements.txt
   ```
4. Run uvicorn
   ```sh
   uvicorn main:app --reload
   ```
5. Open the link generated in the terminal on a browser  
   ```sh
   http://127.0.0.1:8000/docs
   ```

### Alternatively
1. his Api has been hosted on render.com To test, follow the link below.

   ```sh
   https://ezzy-blog-api.onrender.com/docs
   ```

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

[![Ezzy blog screenshot pg1][Ezzy-blog-screenshot-pg1]](https://github.com/mike-eziefule/Ezzy_Blog_api/blob/main/images/ezzy_blogpage1.png)
[![Ezzy blog screenshot pg2][Ezzy-blog-screenshot-pg2]](https://github.com/mike-eziefule/Ezzy_Blog_api/blob/main/images/ezzy_blogpage2.png)

<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/mike-eziefule/CRUD-bank-app/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

X [Formally Twitter] - [@EziefuleMichael](https://twitter.com/EziefuleMichael)

Project Link: [Ezzy_Blog_api](https://github.com/mike-eziefule/CRUD-bank-app)

Email Address: [mike.eziefule@gmail.com](mailto:mike-eziefule@gmail.com)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://engineering.altschoolafrica.com/)
* [Caleb Emelike's FastAAPI Lessons](https://github.com/CalebEmelike)
* [GitHub Student Pack](https://education.github.com/globalcampus/student)
* [Canva](https://www.canva.com/)
* [Stack Overflow](https://stackoverflow.com/)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/mike-eziefule/CRUD-bank-app
[contributors-url]: https://github.com/mike-eziefule/CRUD-bank-app/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mike-eziefule/CRUD-bank-app
[forks-url]: https://github.com/mike-eziefule/CRUD-bank-app/network/members
[stars-shield]: https://img.shields.io/github/stars/mike-eziefule/CRUD-bank-app
[stars-url]: https://github.com/mike-eziefule/CRUD-bank-app/stargazers
[issues-shield]: https://img.shields.io/github/issues/mike-eziefule/CRUD-bank-app
[issues-url]: https://github.com/mike-eziefule/CRUD-bank-app/issues
[license-shield]: https://img.shields.io/github/license/mike-eziefule/CRUD-bank-app
[license-url]: https://github.com/mike-eziefule/CRUD-bank-app/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/follow/EziefuleMichael
[twitter-url]: https://twitter.com/EziefuleMichael
[Ezzy-blog-screenshot-pg1]:images/ezzy_blogpage1.png
[Ezzy-blog-screenshot-pg2]:images/ezzy_blogpage2.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[fastapi]: https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=black
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
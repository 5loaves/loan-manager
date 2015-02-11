loan-manager
============

# Kiva Loan Manager

This open source software is designed to manage micro-loans to report back Kiva. This software was specifcally designed for a non-profit organization focusing on India ([Five Loaves, Two Fish] [1]). The main goals of this project are to

  - Manage the loans following Kiva's standards
  - Work regardless of internet connectivity
  - Sync data accross multiple computers

### Version
0.1

### Desgin
Because Five Loaves, Two Fish is targetting rual India, the internet connection is spotty and unreliable. Thus, I designed this software to work regardless of internet connectivity, but still be able to sync data. To accomplish this, I used a SQLite database and Dropbox to sync it. This has obvious drawbacks, such as conflicting versions of the database, however, it is the best viable solution. We do have restrictions within the organization to minimize the possiblitiy of a database conflict. Other than that, it uses
* Python 2.7 - powers the backend, connects to the database and processes all the data
* SQLite - stores the data
* Javascript/jQuery - front-end scripting for displaying data and interaction
* HTML/CSS - front-end library
* PDF.js - rendering PDFs of loan applications and payment receipts
* Bootstrap - basic layout and formatting

This stack was chosen because it will be easy to extend to a full web application for other Kiva partners who do not have the same internet restrictions. A full web app could easily be launched by switching the SQLite database for MySQL or PostgreSQL, or any other standard SQL database.

### Todo
Tasks still left to be finished:

* Dropbox API integration to sync the database
* Ability to connect a dropbox account
* Testing, usability testing, UI refinement, etc
* Installer for windows (for standard, non-technical users)

### Installation

This relies on Python and webkit (full windows installation coming soon..)

### Development

Want to contribute? Great!

Checkout the Wiki for screenshots and more information!


License
----

MIT


[1]:http://www.5-loaves.org/


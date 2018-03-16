# Studeals
---
- **Institution**: University of Glasgow
- **Academic Year**: 2017/18
- **Course**: Web Application Development 2
- **Team**: Lab 9 Team A
- **Coursework name**: Project
- **Developers**: [Ivan Delev](mailto:2262800d@student.gla.ac.uk), [Ibrahim Javed](mailto:2265799j@student.gla.ac.uk), [Aleksej Panfilov](mailto:2205693p@student.gla.ac.uk), [Luca Vizzarro](mailto:2252593v@student.gla.ac.uk)
- **License**: [MIT](https://opensource.org/licenses/mit-license.php)

## Requirements

- Python 3.6
- Django (web framework)
- Pillow
- Node.js with NPM (for js and css)

## Instructions

Using PIP install the required libraries:
```
pip install Django Pillow
```
Before running the application, the assets need to be compiled. Using npm it is needed to download the dependencies first. Run the following command in the project directory:
```
npm install
```
This should create a new subfolder `node_modules` with all the dependencies inside. Finally, compile the assets with the following command in the project directory. (Use `dev` for development mode, to get easy access in the browser development mode to the actual file, use `build` for the production mode and final version)
```
npm run dev|build
```
Launch the development web server with the following command, to test the app:
```
./manage.py runserver
```
## Description

This project is made for educational purposes as part of the WAD2 coursework.
The main function of this web application is to provide a website where students can share and get easy access to local student deals.

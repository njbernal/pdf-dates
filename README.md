# PDF Date Extractor

A tool to extract dates from PDF files and visualize them on a calendar.
<br /><br />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40" style="margin-right: 10px" />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vuejs/vuejs-original-wordmark.svg" alt="vuejs" width="40" height="40"/>

<br />

# Usage

Load PDF files using the provided button. The app will extract dates from each PDF and then display them both as a list as well as in the calendar. The calendar will be automatically updated to the first date in the topmost file. Adding subsequent files will cause the calendar to jump to the first date in the new file.
<br />
<br />
Clicking the event in the calendar will open a full screen popup with information about where in the PDF the date was extracted from, and provide the user with the option to look at the PDF directly.

<br />

# Testing Options

## Locally with Docker

- `npm run docker` will rebuild both server and client images without cache, and run them.
- `docker compose up` will run both images.
  <br />
  The server will launch on _port 5000_ and client on _port 80_. These commands will default to run the Vue application in dev mode. If you would like to run it in production mode (which uses the remote GCP server), build the image from the ./client/Dockerfile.prod file instead.

## Live version on GCP

Live version: https://pdf-dates-client-eflldgeu2a-uw.a.run.app/

# LifePrioritizationSurvey

## Project Overview
This project explores ethical decision-making in life prioritization through a web-based interactive survey and story, aiming to gather insights into the factors people consider when faced with life-and-death decisions.

## Contributors
- Amir Mann
- David Rudebjer
- Micah Granadino

## Directory Structure
.
├── entries.csv # Database file containing survey and game responses
├── HTMLs # Directory containing all HTML files for the website
│   ├── dry_survey.html # Survey page to collect user's ethical priorities
│   ├── interactive_story.html # Interactive story for the user's decision-making
│   ├── statistics.html # Page to display user decisions and statistics
│   └── images # Directory containing images used in the HTML files
├── README.md # The file you are currently reading
└── server.py # Python script for the backend server


### HTMLs/images Directory
Contains images and data.json for the interactive story and survey, as well as design assets.

## Implementation

### Backend
- `server.py`: Handles backend operations including serving web pages and images, processing survey and game data, and tracking user sessions with unique IDs.
- `entries.csv`: A CSV file acting as the database to store user responses and decisions.

### Frontend
- `HTMLs/dry_survey.html`: Entry point for users, presenting a survey to gauge ethical priorities.
- `HTMLs/interactive_story.html`: Follows the survey, where users make life prioritization decisions.
- `HTMLs/statistics.html`: Displays aggregated results from all users, comparing individual choices to overall trends.

## Running the Project

To host the server, use the command:
`python server.py`
Ensure you have Python 3.6+ installed on a Linux machine. Run `server.py` to start the backend server which hosts the survey and interactive story. Access the survey within the KAIST network to begin the experiment.
The port which the server serves on could be modified with server.py file. Right now it is set to 18080.

## Security and Design Notes
- The current implementation runs over HTTP; future improvements could include transitioning to HTTPS.
- Design improvements and a mobile-optimized version are planned for better user experience.

## Extensions and Future Work
- Extension of the experiment duration and accessibility from a public domain on a standard port.
- Resolution of security issues and improvement of graphical design.
- Enhancements for interactive decision recording and storage.
- Development of a fully functional mobile version.

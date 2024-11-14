# Git Commit Activity Generator

Automate the creation of git commits over a specified date range with customizable options for commit frequency, commit times, and more. This script helps you simulate activity in a repository by generating commits according to your specified parameters, which can be useful for testing, demonstrations, increase privacy or populating a repository's history.

## Features

- **Date Range Specification**: Define the start and end dates for commit generation.
- **Percentage of Active Days**: Specify the percentage of days within the date range on which commits should be created.
- **Customizable Commit Frequency**: Set an exact number of commits per day or define a random range with minimum and maximum commits.
- **Time Interval Control**: Define specific time intervals during the day when commits should be made.
- **Branch Management**: Automatically creates and switches to a specified branch for commit generation.
- **Safety Checks**: Ensures that the script is run in a git repository with a clean working directory.
- **Interactive Configuration**: User-friendly prompts guide you through the setup process.

## Prerequisites

- **Git**: Ensure that Git is installed and properly configured on your system.
- **Python 3**: The script is written in Python 3 and requires Python 3.6 or higher.
- **Git Repository**: The script must be run in the root directory of an existing git repository.

## Installation

1. **Clone the Repository** (or copy the script into your existing repository):

   ```bash
   git clone https://github.com/annyedge/github-activity-python-script.git
   ```

2. **Navigate to the Repository Directory**:

   ```bash
   cd github-activity-python-script
   ```

3. **Make the Script Executable** (optional):

   ```bash
   chmod +x main.py
   ```

## Usage

Run the script from the root directory of your git repository:

```bash
python3 main.py
```
or
```bash
./main.py
```

Follow the interactive prompts to configure the commit generation according to your preferences.

### Example

- **Branch Name**: `feature-commit-generator`
- **Start Date**: `2023-02-01`
- **End Date**: `2023-02-28`
- **Percentage of Days**: `50`
- **Time Intervals**:
  - Enter `09:00 17:00`
  - Enter `22:00 23:50`
  - Enter `done`
- **Exact Number of Commits per Day**: Leave blank.
- **Minimum Commits per Day**: `1`
- **Maximum Commits per Day**: `3`
- **Push to Remote**: Enter `y` to push to the remote repository.

## Configuration Options

- **Branch Name**: The script will create and switch to this branch for commit generation. Default is `activity-branch`.

- **Date Range**:
  - **Start Date**: The date from which to start generating commits (`YYYY-MM-DD`).
  - **End Date**: The date on which to stop generating commits (`YYYY-MM-DD`).

- **Percentage of Days**: The percentage of days within the date range on which commits will be created. Accepts a value between `0` and `100`. Default is `100%`.

- **Time Intervals**: Define one or more time intervals during the day when commits can be made. Intervals are entered in the format `HH:MM HH:MM` (24-hour format). For example:
  - `09:00 12:00` (from 9 AM to 12 PM)
  - `14:00 17:30` (from 2 PM to 5:30 PM)

- **Commits per Day**:
  - **Exact Number**: Specify an exact number of commits to be made each day.
  - **Random Range**: Define a minimum and maximum number of commits per day to randomize commit frequency.
    - **Minimum Commits per Day**: Default is `1`.
    - **Maximum Commits per Day**: Default is `6`.

- **Push to Remote**: Optionally push the generated commits to the remote repository. The script uses `--force` and sets the upstream branch.

## License

I don't care about licenses—do whatever you want!

---

**Disclaimer**: Use this script responsibly. Automating commits can alter your repository's history and may have implications when collaborating with others. Always ensure that force-pushing to a remote repository will not disrupt other collaborators.

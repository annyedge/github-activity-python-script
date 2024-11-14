#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import random

def yes_or_no(question):
    yes_responses = {'y', 'yes', 'o', 'oui'}
    no_responses = {'n', 'no', 'non'}
    while True:
        yn = input(f"{question} [y/n]: ").strip().lower()
        if yn in yes_responses:
            return True
        elif yn in no_responses:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def input_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")

def input_positive_int(prompt, allow_zero=False):
    while True:
        value_str = input(prompt).strip()
        if value_str == '':
            return None
        try:
            value = int(value_str)
            if value >= 0 if allow_zero else value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def input_percentage(prompt):
    while True:
        value_str = input(prompt).strip()
        if value_str == '':
            return 100.0  # Default to 100% if no input
        try:
            value = float(value_str)
            if 0 <= value <= 100:
                return value
            else:
                print("Please enter a percentage between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

def input_time_intervals():
    intervals = []
    print("\nDefine the time intervals during which commits will be created.")
    print("Enter intervals in the form 'HH:MM HH:MM' (24-hour format).")
    print("Enter 'done' when you are finished entering intervals.")
    while True:
        interval_str = input("Enter a time interval or 'done': ").strip()
        if interval_str.lower() == 'done':
            if intervals:
                return intervals
            else:
                print("You must enter at least one interval.")
                continue
        parts = interval_str.split()
        if len(parts) != 2:
            print("Invalid format. Please enter start and end times separated by a space.")
            continue
        start_str, end_str = parts
        try:
            start_time = datetime.datetime.strptime(start_str, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_str, '%H:%M').time()
            if start_time >= end_time:
                print("Start time must be before end time.")
                continue
            intervals.append((start_time, end_time))
        except ValueError:
            print("Invalid time format. Please use 'HH:MM' (24-hour format).")
    return intervals

def get_random_time_within_intervals(intervals):
    # Flatten the intervals into total seconds since midnight
    total_seconds_intervals = []
    for start, end in intervals:
        start_seconds = start.hour * 3600 + start.minute * 60
        end_seconds = end.hour * 3600 + end.minute * 60
        total_seconds_intervals.append((start_seconds, end_seconds))

    # Calculate the total available seconds
    total_available_seconds = sum(end - start for start, end in total_seconds_intervals)

    if total_available_seconds == 0:
        return None  # No available time

    # Choose a random second within the available intervals
    random_second = random.randint(0, total_available_seconds - 1)

    # Find the interval that this second falls into
    accumulated = 0
    for start, end in total_seconds_intervals:
        interval_duration = end - start
        if accumulated + interval_duration > random_second:
            # Calculate the exact time
            seconds_into_interval = random_second - accumulated
            total_seconds = start + seconds_into_interval
            hour = total_seconds // 3600
            minute = (total_seconds % 3600) // 60
            second = total_seconds % 60
            return datetime.time(hour=hour, minute=minute, second=second)
        accumulated += interval_duration
    return None  # Should not reach here

def main():
    # Ensure we're in a git repository
    if not os.path.isdir('.git'):
        print("Error: This script must be run in a git repository.", file=sys.stderr)
        sys.exit(1)

    # Ensure working directory is clean
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, text=True)
    if result.stdout.strip() == '':
        print("OK. Working directory clean...")
    else:
        print("Error: Working directory not clean. Please commit or stash your changes before running this script.", file=sys.stderr)
        sys.exit(2)

    # Prompt user for branch name
    default_branch = 'activity-branch'
    branch_name = input(f"Enter the branch name to use (default: '{default_branch}'): ").strip() or default_branch

    # Switch to the specified branch, create if it doesn't exist
    result = subprocess.run(['git', 'rev-parse', '--verify', branch_name],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        # Branch doesn't exist, create it
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
    else:
        # Branch exists, switch to it
        subprocess.run(['git', 'checkout', branch_name], check=True)

    # Create .commits directory if it doesn't exist
    if not os.path.isdir('.commits'):
        os.makedirs('.commits')

    changes_file = '.commits/changes'
    if not os.path.isfile(changes_file):
        open(changes_file, 'a').close()

    # Ask user for start and end dates
    print("\nPlease enter the date range for commits:")
    while True:
        start_date = input_date("Enter the start date (YYYY-MM-DD): ")
        end_date = input_date("Enter the end date (YYYY-MM-DD): ")
        if start_date <= end_date:
            break
        else:
            print("Error: Start date cannot be after end date. Please re-enter the dates.")

    # Ask user for percentage of days to create commits
    print("\nSpecify the percentage of days on which commits will be created.")
    percentage_days = input_percentage("Enter the percentage of days to create commits (default is 100%): ")

    # Ask user for time intervals
    time_intervals = input_time_intervals()

    # Ask user for number of commits per day
    print("\nConfigure the number of commits per day.")
    print("You can set an exact number of commits per day, or specify a maximum number for random commits per day.")
    exact_commits = input_positive_int("Enter the exact number of commits per day (leave blank to use random): ")
    max_commits = None
    min_commits = None
    if exact_commits is None:
        min_commits = input_positive_int("Enter the minimum number of commits per day (default is 1): ")
        if min_commits is None:
            min_commits = 1  # Default minimum commits per day
        max_commits = input_positive_int("Enter the maximum number of commits per day (default is 6): ")
        if max_commits is None:
            max_commits = 6  # Default maximum commits per day
        if min_commits > max_commits:
            print(f"Swapping min and max commits since {min_commits} > {max_commits}")
            min_commits, max_commits = max_commits, min_commits

    delta = datetime.timedelta(days=1)
    current_date = start_date
    total_days = (end_date - start_date).days + 1
    commit_days = 0

    while current_date <= end_date:
        day_date = current_date
        # Adjust date to have no time component
        day_date = datetime.datetime.combine(day_date.date(), datetime.time(0, 0))
        # Decide whether to create commits on this day based on the percentage
        if random.uniform(0, 100) <= percentage_days:
            commit_days += 1
            print(f"\nCreating commits for {day_date.strftime('%Y-%m-%d')}")

            if exact_commits is not None:
                commits = exact_commits
            else:
                commits = random.randint(min_commits, max_commits)

            print(f"Creating {commits} commits")
            for i in range(1, commits + 1):
                # Get a random time within the specified intervals
                commit_time = get_random_time_within_intervals(time_intervals)
                if commit_time is None:
                    print("No available time intervals for commits. Exiting.")
                    sys.exit(4)
                # Combine date and time
                commit_datetime = datetime.datetime.combine(day_date.date(), commit_time, tzinfo=datetime.timezone.utc)
                day_str = commit_datetime.strftime('%a, %d %b %Y %H:%M:%S %z')

                content = str(int(commit_datetime.timestamp()))
                with open(changes_file, 'a') as f:
                    f.write(f"{content}-{i}\n")
                subprocess.run(['git', 'add', changes_file], check=True)
                commit_message = f"Commit number {content}-{i}"
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                # Amend the commit date
                subprocess.run(['git', 'commit', '--amend', '--no-edit', '--date', day_str],
                               check=True)
        else:
            print(f"Skipping commits for {day_date.strftime('%Y-%m-%d')} due to percentage setting.")

        current_date += delta

    print(f"\nGenerating commits completed. Created commits on {commit_days} out of {total_days} days.\n")

    if yes_or_no("Do you want to push to remote 'origin'?"):
        subprocess.run(['git', 'push', '--force', '--set-upstream', 'origin', branch_name], check=True)
    else:
        print("OK. You can push to your own remote branch later.")

if __name__ == '__main__':
    main()

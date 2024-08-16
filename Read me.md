# README

## Table of Contents

- [About](#about)
- [Running the App](#running-the-app)
- [Features](#features)
- [Usage](#usage)
- [Notes](#notes)
- [Contact](#contact)

## About

MPM (MyPasswordManager) is a password manager with a built in password generator that stores user data locally using cryptographic encryption from the python Cryptography library with options to backup via Google Drive. This is a **free** software and all that is asked is that if you like the app, please share it with your friends and family!

## Running the App

1. Run the MPM.exe file
2. Create a New User profile which is stored under the profiles directory and is named (username).enc this file is case sensitive.
   - The program accesses the user file under the profiles directory, so please do not rename the directory or change the file type from .enc or you will not be able to access your list of credentials.
   - If the .enc file is renamed then to access said profile again you would need to use the new file's name as the username with the associated password.
3. Once the profile is created, log in under existing user and you can start adding/managing passwords for your different accounts.
4. Each profile is unique and another profile with the same name cannot be made. An error will be thrown and the profile will not be created.

## Features

1. Built-in password generation
2. Multiple user profile support
3. Credentials stored are sorted alphabetically first by site and then user
4. Search function to query credentials under a specific username
5. Data encryption on the user data that is stored locally
6. Clipboard capability to copy password onto the clipboard for a better user experience
7. Options to backup both locally and via google drive

## Usage

- Password generation

  - The password generation functionality is optionally available to you when you are adding a new entry to your list of credentials.
  - There are optional integer inputs that you can specify to the generator if you require your passwords to have a specific number of different categories of characters
    - for example a user can specifically request a password with 2 lower case characters, 1 upper case character, 5 number characters and 0 special characters
  - If no parameters are given the password generatorwill create a password that satisfies the following constraints:
    - at least one lower case character
    - at least one upper case character
    - at least one number character
    - at least special character
    - password is 8-15 characters long
  - Once the generate button is clicked, the password will be generated and copied into your clipboard, which you can then simply paste anywhere you would like.

- Multiple profiles

  - As mentioned briefly above under **Running the App**, to create a profile the you will need to create a username and password for a profile under new user, once this is complete you may access your new profile under existing users with the username and password you have just created and you can then add/edit/delete credentials from your profile.

- Search functionality

  - If you wish to search for a specific username you may have used in the past with a site that was added to your profile, you can use the search area under the list of credentials and enter the username in question in input. Keep in mind that this search is case sensitive.
  - There is no functionality to search via site name, but the credentials are sorted alphabetically by site name and then by username for the respective sites.
  - Once the you no longer wish to view the credentials with the given username you may click the back button to go back to view the entire list of credentials.

- Clipboard functionality

  - If you wuold like to copy the password for a specific site to your clipboard, simply hover over the row that contains the password and right click or mouse button two. This will have the password for that site copied into your clipboard.

- Edit/Delete/Add functionality

  - You can edit, delete or add a credential for a site by first selecting the row with the site, username and password. This will auto populate the commands section in the app with into their respective inputs. Once the fields are populated you can:
    - Make edits to an existing credential and click on the edit button to apply the edits, this will replace the selected credential.
    - Delete any credentials you do not want by clicking the delete button.
    - Use an existing credential to create a new credential by making changes and clicking the add button. This will not replace the selected credential, instead a new credential will be added.
    - **A new credential can be added without selecting a pre-existing credential by simply typing in the input fields in the commands section and clicking add.**
  - Upon any change, the list of credentials will refresh to reflect these changes.
  - The program will ask the user to confirm any alterations to pre-existing credentials.
  - Two credentials with the same site and username cannot exist. 
    - If the user tries to add a new credential matching a pre-existing one, the program will throw an error.
    - If the user edits a pre-existing credential in a way that it matches another pre-existing credential, the program will throw an error. 

- Profile username and password change can be done in the menu after login in the settings tab.

- Backup

  - A user can backup their profile locally via the menu after logging in and selecting **Menu > Backup > Local** Backup in the menu bar. A file explorer window will open and the user will provide the name and select the directory in which they desire to backup.

  - A user is also able to backup via Google drive by selecting **Menu > Backup > Google Drive** after logging in. The internet browser will be opened for the user to login to their google drive account. Once authentication is complete, the user will be able to upload their back up profiles.

  - To use a backup file simply place any backup files into the profile directories and you can login to them using the file name without the extension as the username and the password associated with the backup file.

  - If the user prefers to sever the current link to their google drive, either for security reasons or to link with a different google account, they can select **Menu > Backup > Google Drive Reset**.

## Notes

- The app saves your profile information on logout and on exit via the close button on the top right corner. However if any unexpected power outages or system error occurs, it does not save in these situations. With this in mind please if there are large amounts of new entries or edits please save your profile periodically via **Settings > Save**.

## Contact

- You can contact the developer via their email at kangcohen@gmail.com
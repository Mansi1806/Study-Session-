
App Description

An app to create and find study sessions on campus. This promotes collaborative learning among students and helps them get better prepared for exams and assignments in challenging classes at Cornell.

Backend requirements met

Used database modeling to store information about study sessions and users. 
Created a many-to-many relationship between study sessions and users.
Deployed to Google Cloud via Docker and Docker Hub.

- Backend Routes

GET
/api/study_groups/
Gets all study sessions
/api/users/
Gets all users
/api/user/<int:user_id>/
Gets a specific user
/api/partners/
Gets all partner postings
POST
/api/study_groups/
Creates a study session
/api/likes/<int:group_id>/
Adds a like to a study session
/api/users/
Creates a user
/api/study_group/<int:group_id>/add/
Add a user to a study session as a participant
/api/partners/
Creates a partner posting
DELETE
/api/study_group/<int:group_id>/
Deletes a study session
/api/partner/<int:id>/
Deletes a partner posting

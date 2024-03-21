# EMIS Data Engineer - Technical Assessment
Oliver Finn


## How to run
- Download the repo and in the main folder run docker compose up --build
- Once built, in the Docker container run
```
python manage.py migrate
```
- To download FHIR data run the command
```
python manage.py process_fhir patient_data/fhir_data
```
- If you would like to run more json file folders or individual files, save them within the cloned project and run "python manage.py process_fhir" followed by the path you saved them on
- To view the data in an excel format go to your localhost and go to /export

## Strategy
Accomplishing the task to the level required for release was not going to be possible within the time limit (at least I hope not). Rather than rushing to get as much done I tried to focus on storing a few models well with interrelational relationships, and set up a solution that would make it easy to add more resource types going forward. To add further resource types you simply need to create a model, add the information to the config and create a DTO. Additional logic may be required in the helper functions for data types that I have not yet had to process.

## if I had more time
- I'd have liked to include more checks, currently the app doesn't check for edge cases like multiple patients in one file
- The app doesn't check whether the patient IDs are correct at different resource levels
- I'd have stored and been able to process more resource types (obviously)
- I’d have liked to have sped up the processing time. To do this I would’ve made use of bulk database actions like bulk create and concurrency
- I’d have liked to have used config settings to create a generic DTO to avoid having to create a new DTO every time new information is added
- There’s potentially a better way of displaying many to many data in the claims tab of the sheet relating to conditions as currently claims are duplicated. In a real life setting this would be solved by collaborating with the analytics team
- Instead of a management command it would've been better to download the files using a clicker on the Front end to select a file. This would better emulate the data teams usage of the app
- I'd have liked to utilise concurrency and bulk create/ update actions to speed up the processing time
- I'd have added more data validation as I have done in the meta of the Patient object
- It would've been great to have more time to plan. I'd have liked to explore the possiblity of whether the config file would've worked better within an object that processed each resource
- I would've gone through all the resource types to ensure that there isn't any data that would be difficult to process using my solution
- I'd have come up with a better way to validate data on choices. My solution seems messy
- I could've made use of a master DTO which other DTOs would inherit from to store common functions
- I'd have added more specific, user friendly error handling
- I'd have written more tests (more info in the tests.py file)
- I'd have included more fields, currently not all are saved in the models although in a real life setting this information would come from the analytics team
- I'd have like to test what happens if you re-run a file more rigorously. I tried to set up the code so that files would be overwritten if present but this currently isn't in the testing

## What would I do differently
- I wouldn't have started using bulk create. Whilst the optimal solution would probably include this, this ate up a lot of time and made the code very messy, so I abandoned it. The best solution would've been to write the code and get it working first before refactoring to include bulk actions if I had time afterwards
- I'd have included the more specific key error handling earlier. I spent a lot of time trying to figure out why some JSON fields weren't getting looked as the key errors I was getting weren't very helpful. It was only after a while I had the idea to raise my own errors which gave me more information and allowed me to solve the problem quicker

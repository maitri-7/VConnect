# Vconnect
## A portal to inter-connect citizens and hospitals

<img src="https://raw.githubusercontent.com/maitri-7/VConnect/main/logo.png" />

## Testing credentials for checking
- Username: maitrivora password:maitrivora (is_Hospital)
- Username: keshavthosar password:keshavthosar (is_Hospital)
- Username: siddharthmohanty password:siddharthmohanty (is_Citizen)

## Features

- Interconnecting all the citizens and hospitals so that citizens get a transparent inside view of hospitals and can then decide their visit accordingly.
- Proper sharing and management of goods such as beds and cylinders between. hospitals to maintain a uniform flow of logistical distribution.
- Citizens can check their covid-19 diagnosis easily with a click of a single button.
- Citizens can check the live updates of number of Current/Death/Cured cases region wise. 
- Proper analysis of how the cases are rising inside the hospital.

*For hospitals:*
The portal connects every other hospital to suffice their logistical needs such as lack of oxygen cylinders, beds etc. The portal also facilitates proper interaction between hospitals by keeping proper track of each hospital's requests(asked/received).Each hospital can look at the status of every other hospital and can accordingly request the hospitals who are in a condition to donate.

- Send a logistical request to another hospital(beds, oxygen cylinders)
- Approve/Send Mail to establish connection between receiver and donator

*For citizens:*
The portal also predicts the percentage wise probability of the user being infected with COVID-19
Users can also keep track of the hospitals and add them to the watchlist so that they can keep a track of the hospitals easily. Users can select the hospitals on the bases of ratings given by the fellow patients.   

- Adding hospitals to watchlist to keep a better track.
- Checking covid-19 diagnosis based on factors such as sore_throat, age greater than 60, fever, headache, etc.


## Tech Stack Used

We used the following tech-stack:

- [Django] - Main Backend Framework
- [Bootstrap] - Front-end
- [jQuery] - Front-end
- [SciKit-Learn] - Covid-19-diagnosis and providing a probability percentage of the person being infected with covid-19
- [API] - Covid-19 dashboard

## Implementation strategy
https://whimsical.com/tech-a-thon-Vg9gPLqJp8d8EzNa54nHSm

*Basic Website Flow(Citizens):*
- The Citizen will sign up and while signing up will provide his/her health details such as sore_throat, cough, head_ache, etc.
- After logging in the user can then check his/her covid-19 diagnosis predicting details from the User profile page.
- The user can visit the Hospital details page and look at the hospitals around them and add them to their wish list and keep a proper track on them so that when they login the next time they can easily keep track on some of their hospitals so that they can decide their visit to hospitals accordingly.

*Basic Website Flow(Citizens):*
- The Hospital will login and add their logistics details such as beds,O2 cylinders, etc.
- The hospital on a daily basis has to update the number of cases and any change in logistics by going to the update page.
- The hospital can request any other hospital for beds and CO2 and keep track of their requests by going to the My Requests page.
- The hospital to whom we requested can then approve/decline the request and if approved can then send a mail to the admin of that hospital for further process.

   [Bootstrap]: <https://getbootstrap.com/docs/4.3/getting-started/introduction/>
   [jQuery]: <http://jquery.com>
   [Django]:<https://www.djangoproject.com/>
   [SciKit-Learn]:<https://scikit-learn.org/>

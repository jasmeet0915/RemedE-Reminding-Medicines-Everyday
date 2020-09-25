# Remed-E: Reminding Medicines Everyday

This project aims at providing an **ecosystem of intelligent and user-friendly services based on modern samrt home devices and other technologies** that can help patients adhere better to their medicines and become more self-aware **about their side effects and usage**.

The project also includes a **subscriber-based** mechanism which will provide relatives and doctors **quick and easy access to patient's medical history** in cas of emergency.

## Technologies Used:
<ol>
<li>A Java/Kotlin based Android App as the frontend
<li>Google Firebase Realtime Database for backend
<li>Deep Learning based Optical Character Recognition with OpenCV & Java
<li>Custom built Alexa Skill in python for Amazon Echo Device and other Amaxon Alexa based devices.
</ol>

## Data Flow Diagram:
<img src="https://user-images.githubusercontent.com/23265149/94280303-dbf36880-ff6a-11ea-939a-dc2f4bc25de7.jpg" width="600"/>

## The Alexa Skill:

The alexa skill is a custom-hosted skill built with python using <code>ask-sdk-core</code>  and <code>flask-ask-sdk</code>(to route the requests sent by alexa to our skill using a flask app). The endpoint for the skill is obtained by deploying it with ngrok. The skill makes use of <code>firebase_admin</code> python module to get data from firebase backend. The interaction model for the alexa skill including all the intents, their utterances, slots, slot types and dialog model can be found in <code>remede-alexa-skill/assets/interaction_model.json</code>



## Skill Setup Instructions:

1) Create a new skill on amazon developer console and use the <code>assets/interaction_model.json</code> to create the interaction model for the skill using the JSON Editor.

2) Create a new python virtual environment, navigate to <code>remedE-alexa-skill</code> directory and install all the dependencies with <code>pip install -r requirements.txt</code> 

3) Run the <code>remede-skill.py</code> file which runs as a flask app on port 5000 on your localhost.

4) Download [ngrok](https://www.ngrok.com) and run it with protocol set to http and port number 5000.

5) Copy the generated url and paste it in the https endpoint for the skill and then you are ready to test the skill.
 

## How the Skill Works:

1) **LaunchRequest Intent**:
The LaunchRequest Intent invokes when the user says *"Launch Remedy Helper"*. This intent is handled by <code>LaunchRequestHandler</code> which returns a JSON response to alexa cloud with a welcome message including a brief description of the skill and how to begin.

2) **LoginIntent**:
The LoginIntent invokes when the user asks the skill to *"login for user USERNAME"* or *"provide medical adherence for USERNAME"*. This intent is handled by <code>LoginIntentHandler</code> which fetches the user key from the realtime database using the <code>Utils.get_user_key()</code> method. This method then stores the user name and key in json file for later reference. The handler also checks for existing medicine details using the <code>Utils.get_user_medicine_details()</code> method. If medicines are found in the user's data, then the skill returns JSON response to alexa cloud with a welcome message and a question asking permission to set reminders for all the medicines else the skill returns a response with just a welcome message.

3) **AMAZON.YesIntent**:
The Amazon.YesIntent is built-in intent which is invoked when the user says *"Yes"* or its synonyms. This intent is handled by the <code>CreateMedicineReminderHandler</code> which makes an API call to the alexa Reminders API to set daily reminder for all the medicines at the times entered by the user. The skill then returns a JSON response with a confirmation message which then spoken by alexa device.

4) **GetMedDataIntent**:
The GetMedDataIntent is invoked when the user asks the skill to *"give a brief description of MEDANME"* or *"what is MEDNAME used for?"*. This intent is handled by the <code>GetMedDataIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot value from the JSON request recieved by the skill. The handler then calls the <code>Utils.get_med_json_data()</code> to get the *"generic_name"* and *"description"* from the <code>assets/med_data.json</code>. The skill then prepares a speech output string for alexa and returns a JSON response to alexa cloud which is then spoken by alexa.

5) **GetSideEffectsIntent**:
The GetSideEffectsIntent is invoked when the user asks the skill *"what can be the side effects fo MEDNAME"*. This intent is handled by the <code>GetSideEffectsIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot value from the JSON reques recieved by the skill. The handler then calls the <code>Utils.get_med_json_data()</code> method to get the *"side_effects"* from the <code>assets/med_data.json</code> for that medicine. The skil then prepares a speech output string for alexa using the side effects and returns a JSON response to alexa cloud which is then spoken by alexa.

6) **GetNextDoseIntent**:
The GetNextDoseIntent is invoked when the user asks the skill *"when is the my next dose of MEDNAME"*. This intent is handled by the <code>GetNextDoseIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot and the calls the <code>Utils.get_next_dose()</code> method. This method then uses the <code>Utils.get_user_med_data()</code> method to get user medicine details from firebase realtime database. From the recieved medicine data, the method then finds closest dose time to the current time for which the user has not taken the medicine and returns it to the handler. The handler then creates a speech output string and returns the JSON response.

7) **GetRemainingStockIntent**:
The GetRemainingStockIntent is invoked when the user asks the skill *"which of my medicines are running out"* or *"which of my medicines are about to finish"*. This intent is handled by the <code>GetRemainingStockIntentHandler</code> which calls the <code>Utils.get_remaining_stock()</code> method which in turn uses the <code>Utils.get_days_left()</code> method to calculate the number of days in which a particular medicine will run out. The handler then creates an ouput speech which tells the user the number of days all the medicines will last and if any of the medicines will last for only 3 days or less, then those medicines are suggested for reordering to the user. The skill then uses *"Intent Confirmation"* using <code>DelegateDirective</code> to ask if alexa should place an order for the medicines. Depending on the user's response, if <code>intent.confirmation_status</code> of the request is equal to <code>IntentConfirmationStatus.CONFIRMED</code>, this intent is chained to <code>ReorderMedicinesIntentHandler</code>. Else if <code>intent.confirmation_status</code> in the request is equal to <code>IntentConfirmationStatus.DENIED</code>, this intent is chained to  <code>AMAZON.StopIntent</code>. The skill then returns the appropriate intent as a <code>DelegateDirective</code> object with the help of <code>add_directive()</code> method in the response.

8) **ReorderMedicinesIntent**:
This intent does not contain any sample utterances in the skill interaction model, but is chained to <code>GetRemainingStockIntent</code> and is invoked when the user replies in affirmation to the its Intent Confirmation. This intent is handled by the <code>ReorderMedicinesIntentHandler</code> which returns the order placement confirmation message and sends a card to the alexa mobile app of the user showing the deatils of order. (Currently this handler does not actually place any orders due to lack of availablity of any trusted online medicines ordering API) 

9) **AMAZON.StopIntent**:
This intent is invoked whenever the user says *"stop"* and is also chained to the <code>GetRemainingStockHandler</code> through which it is invoked when the user denies its Intent Confirmation. It is handled by the <code>CancelOrStopIntentHandler</code> which just returns a goodbye message to the alexa cloud which is then spoken by the alexa device. 

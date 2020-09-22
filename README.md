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
<br><br><img src="https://drive.google.com/file/d/1OQcB2jlh_dKpAJg4zEMcXSeLd1b3mjFB/view?usp=sharing" width="600"/><br>

## How the Alexa Skill Works:

The alexa skill is a custom-hosted skill built with python using <code>ask-sdk-core</code>  and <code>flask-ask-sdk</code>(to route the requests sent by alexa to our skill using a flask app). The endpoint for the skill is obtained by deploying it with ngrok. The skill makes use of <code>firebase_admin</code> python module to get data from firebase backend. The interaction model for the alexa skill including all the intents, their utterances, slots, slot types and dialog model can be found in <code>remede-alexa-skill/assets/interaction_model.json</code>

<ol>
<li> **LaunchRequest Intent**:
The LaunchRequest Intent invokes when the user says *"Launch Remedy Helper"*. This intent is handled by <code>LaunchRequestHandler</code> which returns a JSON response to alexa cloud with a welcome message including a brief description of the skill and how to begin.

<li> **LoginIntent**:
The LoginIntent invokes when the user asks the skill to *"login for user USERNAME"* or *"provide medical adherence for USERNAME"*. This intent is handled by <code>LoginIntentHandler</code> which fetches the user key from the realtime database using the <code>Utils.get_user_key()</code> method. This method then stores the user name and key in json file for later reference. The handler also checks for existing medicine details using the <code>Utils.get_user_medicine_details()</code> method. If medicines are found in the user's data, then the skill returns JSON response to alexa cloud with a welcome message and a question asking permission to set reminders for all the medicines else the skill returns a response with just a welcome message.

<li> **AMAZON.YesIntent**:
The Amazon.YesIntent is built-in intent which is invoked when the user says *"Yes"* or its synonyms. This intent is handled by the <code>CreateMedicineReminderHandler</code> which makes an API call to the alexa Reminders API to set daily reminder for all the medicines at the times entered by the user. The skill then returns a JSON response with a confirmation message which then spoken by alexa device.

<li> **GetMedDataIntent**:
The GetMedDataIntent is invoked when the user asks the skill to *"give a brief description of MEDANME"* or *"what is MEDNAME used for?"*. This intent is handled by the <code>GetMedDataIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot value from the JSON request recieved by the skill. The handler then calls the <code>Utils.get_med_json_data()</code> to get the *"generic_name"* and *"description"* from the <code>assets/med_data.json</code>. The skill then prepares a speech output string for alexa and returns a JSON response to alexa cloud which is then spoken by alexa.

<li> **GetSideEffectsIntent**:
The GetSideEffectsIntent is invoked when the user asks the skill *"what can be the side effects fo MEDNAME"*. This intent is handled by the <code>GetSideEffectsIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot value from the JSON reques recieved by the skill. The handler then calls the <code>Utils.get_med_json_data()</code> method to get the *"side_effects"* from the <code>assets/med_data.json</code> for that medicine. The skil then prepares a speech output string for alexa using the side effects and returns a JSON response to alexa cloud which is then spoken by alexa.

<li> **GetNextDoseIntent**:
The GetNextDoseIntent is invoked when the user asks the skill *"when is the my next dose of MEDNAME"*. This intent is handled by the <code>GetNextDoseIntentHandler</code> which recieves the medicine name as <code>med_name</code> slot and the calls the <code>Utils.get_next_dose()</code> method. This method then uses the <code>Utils.get_user_med_data()</code> method to get user medicine details from firebase realtime database. From the recieved medicine data, the method then finds closest dose time to the current time for which the user has not taken the medicine and returns it to the handler. The handler then creates a speech output string and returns the JSON response.

<li> **GetRemainingStockIntent**:
The GetRemainingStockIntent is invoked when the user asks the skill *"which of my medicines are running out"*
</ol>

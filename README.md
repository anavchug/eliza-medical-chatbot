# eliza-medical-chatbot

## Main Code:
This project requires both Python and MySQL. To populate the database, create a new MySQL schema and import the `diseases.sql` file. In order to run the main program, run the `app.py` file and copy the HTTP address. Paste the address into the browser to run the program.

## Testing:
Testing consisted of a small selection of Pytests located at key parts of the program. The chosen locations are at the end of methods that read data and determine responses. By focusing the tests at these parts, we were able to identify the key location of an error without having tests for each and every bit of code.

## Features:
1. Compares user inout against a custom database to determine if the user has input a symptom
2. Checks to see if the user is agreeing or disagreeing and responds accordingly
3. Checks to see if the user has indicated they have no further symptoms
4. Uses openai to handle all other inputs
5. Uses a combination of matching symptoms and disease incidents per million to determine the order to present diseases to the user

### UI when the user first opens the chatbot
![chatbot1](https://github.com/anavchug/eliza-medical-chatbot/assets/72577896/8ffc4bc0-c2c6-4f0d-a4ba-c9bc2857beee)

### A user describing disease symptoms to the chatbot
![chatbot2](https://github.com/anavchug/eliza-medical-chatbot/assets/72577896/4c72e31a-c0a8-4ac9-b89a-982dbd553c0a)

### Case where a user enters a random non health related input
![image](https://github.com/anavchug/eliza-medical-chatbot/assets/72577896/595598c0-4ad9-49ad-b6b2-a3445d0e8106)

### Final list of predicted diseases with a score for each disease that shows the likelihood
![chatbot3](https://github.com/anavchug/eliza-medical-chatbot/assets/72577896/2388aa92-0206-4404-a8ba-4ceb34c37deb)




### Disclaimer:
This chatbot is intended for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. The chatbot does not have the ability to accurately diagnose diseases or health conditions. The health-related information provided by this chatbot is not comprehensive and does not cover all diseases, ailments, physical conditions, or their treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or received from this chatbot. If you think you may have a medical emergency, call your doctor or emergency services immediately. The chatbot does not recommend or endorse any specific tests, physicians, products, procedures, opinions, or other information that may be mentioned. Reliance on any information provided by this chatbot is solely at your own risk.

import pytest
import app
import database


# Test database connection
def test_database_connection():
    assert database.get_database_connection() is not None


# Test for process_input
@pytest.mark.parametrize("user_input, specific_words, expected_output", [
    ("I have a fever", "fever", "True_fever"),
    ("Sure, I agree", "", "True_yes"),
    ("No, I don't agree", "", "True_no"),
    ("I am done now", "", "False_finished")
])
def test_process_input(user_input, specific_words, expected_output):
    assert app.process_input(user_input, specific_words) == expected_output


# Test for respond
@pytest.mark.parametrize("user_input, expected_output", [
    ("Yes, I have that symptom", "Thank you."),
    ("No, I do not have this", "What you do not have is not as important. Lets focus on symptoms you do have."),
    ("This code will fail", "this code will fail? Thank you"),
])
def test_respond(user_input, expected_output):
    assert app.respond(user_input) == expected_output


# Test clean symptoms list
def test_clean_symptoms_list():
    symptoms = ((' Runny nose', 5), ('Sneezing', 4), (' Itchy eyes', 4),
                (' Watery eyes', 4), (' Fatigue', 4), ('Stuffy nose', 3))
    assert app.clean_symptoms_list(symptoms) == " Runny nose,Sneezing,Itchy eyes,Watery eyes,Fatigue,Stuffy nose "

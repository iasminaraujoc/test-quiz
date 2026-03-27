import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)

    choice = question.choices[0]
    assert len(question.choices) == 2
    assert choice.text == 'a'
    assert not choice.is_correct

    choice = question.choices[1]
    assert choice.text == 'b'
    assert choice.is_correct

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*201, False)
    with pytest.raises(Exception):
        question.add_choice('a'*500, False)

def test_remove_choice_by_id():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    with pytest.raises(Exception):
        question.remove_choice_by_id('invalid_id')

    assert len(question.choices) == 2

def test_remove_choice_by_nonexistent_id():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    with pytest.raises(Exception):
        question.remove_choice_by_id('nonexistent_id')

    assert len(question.choices) == 2

def test_remove_all_choices():
    question = Question(title='q1')
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_remove_all_choices_on_empty_question():
    question = Question(title='q1')
    
    question.remove_all_choices()

    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)

    question.set_correct_choices([choice1.id, choice2.id])

    assert choice1.is_correct
    assert choice2.is_correct
    assert not choice3.is_correct

def test_set_correct_choices_with_invalid_id():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    with pytest.raises(Exception):
        question.set_correct_choices(['invalid_id'])

    assert not choice1.is_correct
    assert not choice2.is_correct

def test_set_correct_choices_with_empty_list():
    question = Question(title='q1', max_selections=2)
    
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    question.set_correct_choices([])

    assert not choice1.is_correct
    assert not choice2.is_correct

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', False)
    return question, choice1, choice2, choice3

def test_correct_selected_choices(question_with_choices):
    question, choice1, choice2, choice3 = question_with_choices

    selected_choice_ids = [choice1.id, choice2.id]
    correct_choice_ids = question.correct_selected_choices(selected_choice_ids)

    assert correct_choice_ids == [choice2.id]

def test_correct_selected_choices_with_invalid_id(question_with_choices):
    question, choice1, choice2, choice3 = question_with_choices

    selected_choice_ids = ['invalid_id']
    
    assert question.correct_selected_choices(selected_choice_ids) == []
from app.utils.date_parser import get_date
def test_new_user(make_new_task):
    title = "Test Task"
    description = "Run test for new task"
    duedate = get_date("2020-08-12")
    assert make_new_task.Title == title
    assert make_new_task.Description == description
    assert make_new_task.DueDate == duedate
from datetime import datetime


def sort_list_by_time(seq, pst):
    """ Sorterar listor sett till tid """
    if not seq:
        seq.append(pst)
        return seq
    elif seq[0]['time'] >= pst['time']:
        seq.insert(0, pst)
        return seq
    else:
        return [seq[0]] + sort_list_by_time(seq[1:], pst)


def validate_user_data(param, data):
    """ Validerar att informationen som skickas in i user är tillåtna """
    false_message = 'Wrong input'
    if param == 'name':
        if 2 <= len(data) <= 50:
            return True
        false_message = 'Name must be between 1 and 51 characters'
    elif param == 'gender':
        if data == 'Male' or data == 'Female' or data == 'Not certain':
            return True
        false_message = 'Gender not correct'
    elif param == 'email':
        from golfbuddy.models import User
        is_email = User.query.filter_by(email=data).first()
        if is_email is None:
            return True
        false_message = 'This email already has an account'
    elif param == 'hcp':
        if not float(data):
            false_message = "HCP must be in th form 1.0"
        else:
            if -4.0 <= float(data) <= 54.0:
                return True
            false_message = 'Not valid HCP'
    elif param == 'password':
        if 8 <= len(data) <= 100:
            return True
        false_message = 'Password must be between 7 and 101 characters'
    elif param == 'birthdate':
        try:
            datetime.strptime(data, "%Y-%m-%d")
            return True
        except ValueError:
            false_message = 'Not correct date'
    if false_message == "Wrong input":
        print(param, data)
    return false_message

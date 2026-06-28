import time
import datetime

def do_math_operation_with_numbers(value1, value2, op_type, is_advanced):
    
    if op_type == 'add':
        if is_advanced == True:
            result = value1 + value2 + 100
            return result
        else:
            result = value1 + value2
            return result
    elif op_type == 'sub':
        if is_advanced == True:
            result = value1 - value2 - 100
            return result
        else:
            result = value1 - value2
            return result
    elif op_type == 'mul':
        if is_advanced == True:
            result = value1 * value2 * 100
            return result
        else:
            result = value1 * value2
            return result
    elif op_type == 'div':
        if value2 != 0:
            if is_advanced == True:
                result = value1 / value2 / 100
                return result
            else:
                result = value1 / value2
                return result
        else:
            return 0
    else:
        return 0

def calculate_advanced_and_basic_stuff_again(value1, value2, op_type, is_advanced):
    
    if op_type == 'add':
        if is_advanced == True:
            result = value1 + value2 + 100
            return result
        else:
            result = value1 + value2
            return result
    elif op_type == 'sub':
        if is_advanced == True:
            result = value1 - value2 - 100
            return result
        else:
            result = value1 - value2
            return result
    elif op_type == 'mul':
        if is_advanced == True:
            result = value1 * value2 * 100
            return result
        else:
            result = value1 * value2
            return result
    elif op_type == 'div':
        if value2 != 0:
            if is_advanced == True:
                result = value1 / value2 / 100
                return result
            else:
                result = value1 / value2
                return result
        else:
            return 0
    else:
        return 0

class UserManager:
    

    def process_usr_lst_data_complex(self, lst_of_usr_dicts, include_admins, filter_by_age, min_age_thresh):
        
        final_processed_usr_lst = []
        for user in lst_of_usr_dicts:
            if user['is_active'] == True:
                if include_admins == True:
                    if filter_by_age == True:
                        if user['age'] >= min_age_thresh:
                            user['processed_at'] = str(datetime.datetime.now())
                            user['status'] = 'PROCESSED_ACTIVE_ADMIN_AGE_FILTERED'
                            final_processed_usr_lst.append(user)
                        else:
                            pass
                    else:
                        user['processed_at'] = str(datetime.datetime.now())
                        user['status'] = 'PROCESSED_ACTIVE_ADMIN_NOT_AGE_FILTERED'
                        final_processed_usr_lst.append(user)
                elif user['role'] != 'admin':
                    if filter_by_age == True:
                        if user['age'] >= min_age_thresh:
                            user['processed_at'] = str(datetime.datetime.now())
                            user['status'] = 'PROCESSED_ACTIVE_NO_ADMIN_AGE_FILTERED'
                            final_processed_usr_lst.append(user)
                        else:
                            pass
                    else:
                        user['processed_at'] = str(datetime.datetime.now())
                        user['status'] = 'PROCESSED_ACTIVE_NO_ADMIN_NOT_AGE_FILTERED'
                        final_processed_usr_lst.append(user)
            else:
                pass
        return final_processed_usr_lst

def main():
    
    a1 = do_math_operation_with_numbers(10, 5, 'add', False)
    a2 = calculate_advanced_and_basic_stuff_again(10, 5, 'add', False)
    print('res 1:', a1)
    print('res 2:', a2)
    manager = UserManager()
    data = [{'name': 'Alice', 'role': 'admin', 'age': 30, 'is_active': True}, {'name': 'Bob', 'role': 'user', 'age': 20, 'is_active': True}, {'name': 'Charlie', 'role': 'user', 'age': 40, 'is_active': False}]
    result = manager.process_usr_lst_data_complex(data, True, True, 25)
    print('processed data:', result)
if __name__ == '__main__':
    main()

import sys
import os
import datetime
import linear_regression
import random_forest
import gradient_boosting

def make_log(log_path:str, exec_func, func_param:dict):
    # mengarahkan stdout dan stderr ke file log
    log_file = open(log_path, 'w', buffering=1)
    sys.stdout = log_file
    sys.stderr = log_file

    start_time = datetime.datetime.now()

    # menjalankan script
    exec_func(**func_param)

    end_time = datetime.datetime.now()
    diff_in_seconds = (end_time - start_time).total_seconds()
    print(f"\nElapsed time for the optimization process: {int(diff_in_seconds//60)} minutes {diff_in_seconds%60:.1f} seconds")

    # Tutup file log
    log_file.close()


if __name__ == '__main__':
    # running script hyperparameter tuning model Linear Regression
    log_path = 'src/hyperparameter_tuning/linear_regression.log'
    exec_func = linear_regression.hyperparameter_tuning
    func_param = {'n_trials': 500}

    if not os.path.exists(log_path):
        make_log(log_path, exec_func, func_param)

    else:
        print(f"The log file {log_path} already exists.")

    # running script hyperparameter tuning model Random Forest Regressor
    log_path = 'src/hyperparameter_tuning/random_forest.log'
    exec_func = random_forest.hyperparameter_tuning
    func_param = {'n_trials': 500}

    if not os.path.exists(log_path):
        make_log(log_path, exec_func, func_param)

    else:
        print(f"The log file {log_path} already exists.")

    # running script hyperparameter tuning model XGBoost Regressor
    log_path = 'src/hyperparameter_tuning/gradient_boosting.log'
    exec_func = gradient_boosting.hyperparameter_tuning
    func_param = {'n_trials': 500}

    if not os.path.exists(log_path):
        make_log(log_path, exec_func, func_param)

    else:
        print(f"The log file {log_path} already exists.")


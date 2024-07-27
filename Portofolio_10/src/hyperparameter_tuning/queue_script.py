import sys
import os
import datetime
import arsitektur_1
import arsitektur_2

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
    # running script hyperparameter tuning model Arsitektur_1
    log_path = 'src/hyperparameter_tuning/arsitektur_1.log'
    exec_func = arsitektur_1.hyperparameter_tuning
    func_param = {'n_trials': 30}

    if not os.path.exists(log_path):
        make_log(log_path, exec_func, func_param)

    else:
        print(f"The log file {log_path} already exists.")

    # running script hyperparameter tuning model Arsitektur_2
    log_path = 'src/hyperparameter_tuning/arsitektur_2.log'
    exec_func = arsitektur_2.hyperparameter_tuning
    func_param = {'n_trials': 30}

    if not os.path.exists(log_path):
        make_log(log_path, exec_func, func_param)

    else:
        print(f"The log file {log_path} already exists.")

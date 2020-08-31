from data_management import *
from compare_versions import run_comparison_workflow
from create_logs import run_logs_workflow


def run_flow():
    # try:
    # add_new_channel(mine=True)
    initialize_folders()

    run_comparison_workflow()
    run_logs_workflow()
    remove_old_version()

    # except Exception as e:
    #     print(e)
    #     remove_all_data()


if __name__ == "__main__":
    run_flow()

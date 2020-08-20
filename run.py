from data_management import remove_old_version, remove_all_data
from compare_versions import run_comparison_workflow
from create_logs import run_logs_workflow


if __name__ == "__main__":

    try:
        run_comparison_workflow()
        run_logs_workflow()
        remove_old_version()

    except Exception as e:
        print(e)
        remove_all_data()

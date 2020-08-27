from data_management import add_new_channel, initialize_folders

if __name__ == "__main__":
    initialize_folders()
    add_new_channel(mine=True, new_client_secrets=True)

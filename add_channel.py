import os

from data_management import add_new_channel, initialize_folders

if __name__ == "__main__":
    initialize_folders()

    # You need to move the client secrets under channel/new_channel to run this
    # add_new_channel(mine=True, new_client_secrets=True)

    add_new_channel(mine=True,
                    new_client_secrets=False,
                    channel_id_secrets=os.environ['MAIN_CHANNEL_ID'])

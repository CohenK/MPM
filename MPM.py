from ui.main_window_ui import Main_Window
from utils.google_drive_util import GoogleDriveClient
from utils import helper

main = Main_Window()
main.run()

# google = GoogleDriveClient()
# google.upload_file(helper.resource_path("Profile/Test.enc"))
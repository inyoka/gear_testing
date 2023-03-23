from customtkinter import *
from PIL import Image



class NavBar(CTkFrame):
    def __init__(self, parent):
        super(NavBar, self).__init__(parent, corner_radius=10, fg_color="transparent")
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../images")


        self.home_image = CTkImage(light_image=Image.open(os.path.join(self.image_path, "home_dark.png")),
        dark_image=Image.open(os.path.join(self.image_path, "home_light.png")), size=(20, 20))

        self.chat_image = CTkImage(light_image=Image.open(os.path.join(self.image_path, "chat_dark.png")),
        dark_image=Image.open(os.path.join(self.image_path, "chat_light.png")), size=(20, 20))

        self.add_user_image = CTkImage(light_image=Image.open(os.path.join(self.image_path, "add_user_dark.png")),
        dark_image=Image.open(os.path.join(self.image_path, "add_user_light.png")), size=(20, 20))

        self.logo_image = CTkImage(Image.open(os.path.join(parent.image_path, "logo.png")), size=(42, 24))

        self.navigation_logo = CTkLabel(self, text="", image=self.logo_image, compound="left")
        self.navigation_logo.grid(sticky="nsew", row=0, column=0, padx=(0, 0), pady=(20,10))


        self.appearance_mode_menu = CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def change_appearance_mode_event(self, new_appearance_mode):
        set_appearance_mode(new_appearance_mode)

    def create_gear_button_event(parent):
        parent.select_frame_by_name("CreateGear")

    def frame_2_button_event(parent):
        parent.select_frame_by_name("PINDIA")

    def frame_3_button_event(parent):
        parent.select_frame_by_name("PINDIA")

if __name__ == "__main__":
    root = CTk()
    root.title("My App")
    # root.image_path = "../images"
    root.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../images")

    
    nav_bar = NavBar(root)
    nav_bar.grid(row=0, column=0, sticky="nsew")
    
    root.mainloop()


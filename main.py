
from nicegui import ui, Client, app
# import pandas as pd
from projectsPage import ProjectsPage

class MainPage(ui.page):
    def __init__(self, path="/"):
        self.expose_drawer = False
        
        super().__init__(path)
        self.add_drawer()
        self.add_header()

        self.index()    

    def add_drawer(self):
        self.drawer = ui.left_drawer()
        text = ["Assignments", "Projects", "Modules"]
        icons = ["assignment", "folder", "menu_book"]
        with self.drawer.style("border: 1px solid black; background-color: lightgray; width: 10vw;"):
            for i in range(3):
                with ui.link(target=f"/{text[i].lower()}").style("width: 100%; text-decoration: none; height: 5vh; margin-left: -15px; margin-top: -15px;"):
                    with ui.row().style("background-color: gray; width: 110%; height: 5vh; border: 1px solid black; display: flex; justify-content: space-between; align-items: center; padding: 0 15px;"):
                        ui.label(text[i]).style("font-size: 1.5em; color: white; margin: 0;")
                        ui.icon(icons[i]).style("font-size: 2em; color: white; margin: 0;")


        self.drawer.hide()

    @ui.page("/assignments")
    def assigments():
        ui.label("Assignments page")
    
    @ui.page("/modules")
    def modules():
        ui.label("Modules page")
    

    @ui.page("/projects")
    def projects():
        ProjectsPage()


        
    def add_header(self):
        self.header = ui.header()
        with self.header:
            ui.button(icon="menu", on_click=lambda :  self.drawer.toggle()).style("left: 0;")
            with ui.button(icon="account_circle").style("right: 2vw; position: absolute;"):
                self.profile_menu = ui.menu()
                with self.profile_menu:
                    labels = ["Profile", "Settings", "Logout"]
                    icons = ["account_circle", "settings", "logout"]
                    for i in range(3):
                        with ui.menu_item().style("width: auto; background-color: lightgray; border: 1px solid black; display: flex; justify-content: space-between; align-items: center; padding: 0 15px;"):
                            with ui.row().style("display: flex; justify-content: space-between; align-items: center; width: 100%;"):
                                ui.label(labels[i]).style("font-size: 1.5em;")
                                ui.icon(icons[i]).style("font-size: 2em;")


            ui.button(icon="help").style("right: 6vw; position: absolute;")

    def index(self):
        self.header







page = MainPage()





ui.run()


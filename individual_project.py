from nicegui import ui, app, Client
import pandas as pd
from project_progress import ProjectProgress

class IndividualPage(ui.page):
    def __init__(self, route):
        self.links = ["New Module", "New Folder", "Manage Servers", "Generate Codec", "Share", "Project Progress"]
        super().__init__(f"/projects_{route.lower().replace(' ', '_')}")
        self.route = route
        self.add_drawer()
        self.add_header()
        self.index()


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

    def add_drawer(self):
        self.drawer = ui.left_drawer()
        text = ["Assignments", "Projects", "Modules"]
        icons = ["assignment", "folder", "menu_book"]
        with self.drawer.style("border: 1px solid black; background-color: lightgray; width: 10vw;"):
            for i in range(3):
                with ui.link(target=f"/{self.route}/{text[i].lower()}").style("width: 100%; text-decoration: none; height: 5vh; margin-left: -15px; margin-top: -15px;"):
                    with ui.row().style("background-color: gray; width: 110%; height: 5vh; border: 1px solid black; display: flex; justify-content: space-between; align-items: center; padding: 0 15px;"):
                        ui.label(text[i]).style("font-size: 1.5em; color: white; margin: 0;")
                        ui.icon(icons[i]).style("font-size: 2em; color: white; margin: 0;")


        self.drawer.hide()
    

    def index(self):
        self.header
        with ui.row().style("width: 90vw; margin-left: 1vw;"):
            ui.label(f"{self.route}").style("font-size: 2em; margin: 0; padding: 0 15px; border: 1px solid black; background-color: lightgray; ")
            # ui.button("+New").style("")
            with ui.button(icon="menu", color="lightgray").style("font-size: 1.2em; background-color: lightgray; border: 1px solid black; padding: 0 15px;"):
                # ui.icon("add").style("font-size: 2em;")
                with ui.menu():
                    for i in range(len(self.links)):
                        with ui.menu_item().style("width: auto; background-color: lightgray; border: 1px solid black; display: flex; justify-content: space-between; align-items: center; padding: 0 15px;"):
                            with ui.link(target=f"/{self.route.lower().replace(' ', '_')}/{self.links[i].lower().replace(' ', '_')}").style("text-decoration: none;"):
                                with ui.row().style("display: flex; justify-content: space-between; align-items: center; width: 100%;"):
                                    ui.label(self.links[i]).style("font-size: 1.5em;")

        df = pd.DataFrame(data={
            'Name' : ['TEASync', 'Codec', 'Main', 'Types'],
            'Last Modified': ['2024-03-04', '2005-05-11', '1999-01-11', '2005-05-11'],
            "Last Commit Message": ["Used Knuth's algorithm instead.. ", "Stuff", "Stuff", "Stuff"]
        })
        icons = ["folder", "folder", "description", "description"]

        table_html = """
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Last Modified</th>
                    <th>Last Commit Message</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in df.iterrows():
            table_html += f"""
            <tr>
                <td><i class="material-icons">{icons[_]}</i>{row['Name']}</td>
                <td>{row['Last Modified']}</td>
                <td>{row['Last Commit Message']}</td>
            </tr>
        """

        table_html += """
            </tbody>
        </table>
        """

        # Add some CSS styling to the table
        style = """
        <style>
        .styled-table {
            width: 80vw;
            border-collapse: collapse;
            font-size: 2.5em;
            font-family: Arial, sans-serif;
            padding-left: 10vw;
            padding-right: 10vw;
        }

        .styled-table th {
            background-color: #f2f2f2;
            border: 1px solid black;
            text-align: left;
        }

        .styled-table td {
            border: 1px solid black;
        }

        .styled-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        .styled-table tr:hover {
            background-color: lightblue;
        }

        .material-icons {
            vertical-align: middle;
        }
        </style>
        """

        # Concatenate the HTML table and styling
        table_html = style + table_html

        # Create a NiceGUI HTML element to display the table
        html_element = ui.html(table_html).style("border: 1px solid black; margin-left: 1vw; margin-top: 2vh;")

        # ui.add_body_html(html_element)

            

    @ui.page("/{route}/project_progress")
    def temp(route):
        ProjectProgress(route)
            
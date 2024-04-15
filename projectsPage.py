from nicegui import ui, Client, app
import pandas as pd
from individual_project import IndividualPage


class ProjectsPage(ui.page):
    def __init__(self):
        super().__init__("/projects")
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
                with ui.link(target=f"/{text[i].lower()}").style("width: 100%; text-decoration: none; height: 5vh; margin-left: -15px; margin-top: -15px;"):
                    with ui.row().style("background-color: gray; width: 110%; height: 5vh; border: 1px solid black; display: flex; justify-content: space-between; align-items: center; padding: 0 15px;"):
                        ui.label(text[i]).style("font-size: 1.5em; color: white; margin: 0;")
                        ui.icon(icons[i]).style("font-size: 2em; color: white; margin: 0;")


        self.drawer.hide()

    def index(self):
        self.header
        with ui.row().style("width: 90vw; margin-left: 1vw;"):
            ui.label("My Projects").style("font-size: 2em; margin: 0; padding: 0 15px; border: 1px solid black; background-color: lightgray; ")
            # ui.button("+New").style("")
            with ui.button("New", color="lightgray").style("font-size: 1.2em; background-color: lightgray; border: 1px solid black; padding: 0 15px;"):
                ui.icon("add").style("font-size: 2em;")
        df = pd.DataFrame(data={
        'Project Name': ["Project 1", "Project 2", "Design Thinking"], 
        'Type': ["TEASync", "TEASync", "TEASync"], 
        'Most Recent Update': ["2024-03-04", "2005-05-11", "1999-01-11"], 
        'Last Commit Message': ["Finished 1XD3 Final exam", "Born", "Random Date?" ]
        })

        js_code = """
        function redirectToRoute(route) {
            window.location.href = "/projects_" + route.toLowerCase().replace(/\s+/g, '_');
        }

        function sortTableByDate() {
            var table = document.getElementById('myTable');
            var rows = table.rows;
            var data = [];

            // Extract and format dates from the table
            for (var i = 1; i < rows.length; i++) {
                var cell = rows[i].cells[2]; // Column index of the date field
                var date = cell.innerHTML;
                var formattedDate = date.split('-').join('');
                data.push({row: rows[i], date: formattedDate});
            }

            // Sort the data based on date in descending order
            data.sort(function(a, b) {
                return b.date.localeCompare(a.date); // Reverse the comparison
            });

            // Reorder the rows in the table
            for (var i = 0; i < data.length; i++) {
                table.appendChild(data[i].row);
            }
        }

        """

        # Generate HTML for the table
        table_html = """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        table th, table td {
            border: 1px solid #999;
            padding: 8px;
            text-align: left;
            font-family: Arial, sans-serif;
            font-size: 1.5em;

        }
        

        table th {
            background-color: #BAD2E3;
            cursor: pointer; /* Add pointer cursor to indicate sortable headers */
            
        }
        table tr:hover {
            background-color: #0D99FF;
        }
        table tr {
            background-color: #BAD2E3;
        }
        </style>

        <table id="myTable">
            <thead>
                <tr>
                    <th onclick="sortTableByDate()">Project Name</th>
                    <th>Type</th>
                    <th>Most Recent Update</th>
                    <th>Last Commit Message</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in df.iterrows():
            table_html += f"""
                <tr onclick="redirectToRoute('{row['Project Name']}')">
                    <td>{row['Project Name']}</td>
                    <td>{row['Type']}</td>
                    <td>{row['Most Recent Update']}</td>
                    <td>{row['Last Commit Message']}</td>
                </tr>
        """

        table_html += """
            </tbody>
        </table>
        """

        # Create a NiceGUI HTML element to display the table
        html_element = ui.html(table_html).style("width: 90vw; margin-left: 1vw;")


        ui.add_body_html("<script>" + js_code + "</script>")
    
    @ui.page("/projects_{project_name}")
    def project_page(project_name):
        project_name = project_name.replace("_", " ")
        project_name = project_name.title()
        
        IndividualPage(project_name)
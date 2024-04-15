
from nicegui import ui, events
from datetime import datetime
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class ProjectProgress(ui.page):
    def __init__(self, route):
        super().__init__(f"/project_progress/{route}")
        self.route = route.replace("_", " ").title()
        self.add_header()
        self.add_drawer()
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
    
    def tasks(self):
        columns = [
            {"name": "task", "label": "Task", "field": "task", "align": "left"},
            {"name": "actions", "label": "", "field": "actions", "align": "left"},
            {"name": "created_at", "label": "Date Created", "field": "created_at", "align": "left"},
            {"name": "assignee", "label": "Assignee", "field": "assignee", "align": "left"},
        ]
        rows = [
            {"id": 0, "task": "Make it so that it updates in real time", "created_at": "11-02-2023", "assignee": "https://cdn.quasar.dev/img/avatar1.jpg" },
            {"id": 1, "task": "finish exam", "created_at": "11-02-2023", "assignee": "https://cdn.quasar.dev/img/avatar2.jpg"},
            {"id": 2, "task": "document", "created_at": "11-02-2023", "assignee": "https://cdn.quasar.dev/img/avatar3.jpg"},
            {"id": 3, "task": "improve ui", "created_at": "11-02-2023", "assignee": "https://cdn.quasar.dev/img/avatar4.jpg"},
            {"id": 4, "task": "stuff", "created_at": "11-02-2023", "assignee": "https://cdn.quasar.dev/img/avatar5.jpg"},
        ]

        def delete(e: events.GenericEventArguments) -> None:
            for row in rows:
                if row["id"] == e.args["row"]["id"]:
                    rows.remove(row)
            table.update()

        def change_status(e: events.GenericEventArguments) -> None:
            delete(e)

        card_opened = False

        def open_card():
            nonlocal card_opened
            with ui.card().style("border: 1px solid black; height: 25vh; width: 30vw; position: absolute; left: 15%") as card:
                card_opened = True
                with ui.row().style("width: 100%; height: 100%;"):
                    with ui.column().style("width: 80%;"):
                        with ui.row().style("width: 100%; height: 40px; background-color: white; margin-bottom: 1vw;"):
                            ui.input(label="Type Task header here").style("background-color: lightblue; width: 100%;")
                        with ui.row().style("width: 100%; height: 100px; background-color: white"):
                            ui.textarea(label="Type error here").style("background-color: lightblue; width: 100%;")
                    with ui.column().style("width: 10%;"):
                        ui.select(["Joe", "Bob", "Janice"], value='Joe')
                        def update_card():
                            nonlocal card_opened 
                            card_opened = False
                            card.set_visibility(False)
                        ui.button("Submit", on_click=lambda : update_card())
                        ui.button("Close", on_click=lambda : update_card())

        create_new_task  = ui.button("Create new task", on_click=lambda :  open_card() if not card_opened else None).style("background-color: lightgray")
        with create_new_task:
            ui.icon("add")
        with ui.row().style("width: 100vw;"):
            table = ui.table(columns=columns, rows=rows).style("width: 100%; height: 100%;")
            table.add_slot(
            "body-cell-actions",
            r"""
            <q-td auto-width key="actions" :props="props" class="w-min">
                <div class="nicegui-row w-min gap-1">
                    <q-btn class="row" @click="$parent.$emit('change_status', props)" :icon="props.row.is_completed ? 'r_highlight_off' : 'r_check_circle_outline'" outline :color="props.row.is_completed ? 'red-6' : 'green-6'" class="leading-normal" flat padding="xs" />
                    <q-btn class="row" @click="$parent.$emit('delete', props)" icon="r_delete" outline color="red-6" class="leading-normal" flat padding="xs"/>
                </div>                
            </q-td>

            """,
            )

            table.add_slot(
                "body-cell-assignee",
                r"""
                <q-td auto-width key="assignee" :props="props" class="w-min">
                    <div class="nicegui-row gap-1" :width="100" :height="100">
                        <img :src="props.row.assignee" :width="100" :height="100"/>
                    </div>
                </q-td>
                """,
            )
            table.add_slot(
                "body-cell-task",
                r"""
                <q-td auto-width key="task" :props="props" class="w-min">
                    <div class="nicegui-row gap-1">
                        <div style="font-size: 1.5em;">{{ props.row.task }}</div>
                    </div>
                </q-td>
                """
            )
            table.add_slot(
                "body-cell-created_at",
                r"""
                <q-td auto-width key="created_at" :props="props" class="w-min">
                    <div class="nicegui-row gap-1">
                        <div style="font-size: 1.5em;">{{ props.row.created_at }}</div>
                    </div>
                </q-td>
                """
            )
            table.add_slot('header', r'''
                <q-tr>
                    <q-th v-for="col in props.cols" :key="col.name" style="background-color: #0D99FF;">
                        <div style="font-size: 1.5em;">{{ col.label }}</div>
                    </q-th>
                </q-tr>
            ''')
            table.style("background-color: lightblue;")
            table.on("delete", delete)
            table.on("change_status", change_status)

    def issues(self):
        columns = [
            {"name": "task", "label": "Issue", "field": "task", "align": "left"},
            {"name": "actions", "label": "", "field": "actions", "align": "left"},
            {"name": "created_at", "label": "Date Created", "field": "created_at", "align": "left"},
        ]
        rows = [
            {"id": 0, "task": "Type Mismatch \n The 1st argument to `encodeList` is not what I expect:  ....  ", "created_at":"11-02-2023" },
            {"id": 1, "task": "Type Mismatch \n The (++) operator cannot append this type of value: ...", "created_at": "11-02-2023"},
            {"id": 2, "task": "Naming Error \n     Cannot find variable 'List.nap' ...", "created_at": "11-02-2023"},
            {"id": 3, "task": "Unfinished Record Type \n     I was partway through this record type, but I got here: ...", "created_at": "11-02-2023",},
        ]

        def delete(e: events.GenericEventArguments) -> None:
            for row in rows:
                if row["id"] == e.args["row"]["id"]:
                    rows.remove(row)
            table.update()

        def change_status(e: events.GenericEventArguments) -> None:
            delete(e)

        card_opened = False
        def open_card():
            nonlocal card_opened
            with ui.card().style("border: 1px solid black; height: 35vh; width: 30vw; position: absolute; left: 15%;") as card:
                card_opened = True
                with ui.row().style("width: 100%; height: 100%;"):
                    with ui.column().style("width: 80%;"):
                        with ui.row().style("width: 100%; height: 40px; background-color: white; margin-bottom: 1vw;"):
                            ui.input(label="Type Task header here").style("background-color: lightblue; width: 100%;")
                        with ui.row().style("width: 100%; height: 100px; background-color: white"):
                            ui.textarea(label="Type error here").style("background-color: lightblue; width: 100%;")
                        with ui.row().style("width: 100%; margin-top: 10%;"):

                            def update_card():
                                nonlocal card_opened 
                                card_opened = False
                                card.set_visibility(False)
                            ui.button("Submit", on_click=lambda : update_card())
                            ui.button("Close", on_click=lambda : update_card())

        create_new_issue  = ui.button("Create new issue", on_click=lambda :  open_card() if not card_opened else None).style("background-color: lightgray;")
        with create_new_issue:
            ui.icon("add")

        with ui.row().style("width: 100vw;"):

            table = ui.table(columns=columns, rows=rows).style("width: 100%; height: 100%;")
            table.add_slot(
            "body-cell-actions",
            r"""
            <q-td auto-width key="actions" :props="props" class="w-min">
                <div class="nicegui-row w-min gap-1">
                    <q-btn class="row" @click="$parent.$emit('change_status', props)" :icon="props.row.is_completed ? 'r_highlight_off' : 'r_check_circle_outline'" outline :color="props.row.is_completed ? 'red-6' : 'green-6'" class="leading-normal" flat padding="xs" />
                    <q-btn class="row" @click="$parent.$emit('delete', props)" icon="r_delete" outline color="red-6" class="leading-normal" flat padding="xs"/>
                </div>                
            </q-td>

            """,
            )

            table.add_slot(
                "body-cell-assignee",
                r"""
                <q-td auto-width key="assignee" :props="props" class="w-min">
                    <div class="nicegui-row gap-1" :width="100" :height="100">
                        <img :src="props.row.assignee" :width="100" :height="100"/>
                    </div>
                </q-td>
                """,
            )
            table.add_slot(
                "body-cell-task",
                r"""
                <q-td auto-width key="task" :props="props" class="w-min">
                    <div class="nicegui-row gap-1">
                        <div style="font-size: 1.5em;">{{ props.row.task }}</div>
                    </div>
                </q-td>
                """
            )
            table.add_slot(
                "body-cell-created_at",
                r"""
                <q-td auto-width key="created_at" :props="props" class="w-min">
                    <div class="nicegui-row gap-1">
                        <div style="font-size: 1.5em;">{{ props.row.created_at }}</div>
                    </div>
                </q-td>
                """
            )
            table.add_slot('header', r'''
                <q-tr>
                    <q-th v-for="col in props.cols" :key="col.name" style="background-color: #0D99FF;">
                        <div style="font-size: 1.5em;">{{ col.label }}</div>
                    </q-th>
                </q-tr>
            ''')
            table.add_slot(
                "body-cell-task",
                r"""
                <q-td auto-width key="task" :props="props" class="w-min" style="white-space: pre-line;">
                    <div class="nicegui-row" style="display:inline-block;">
                        <div style="font-size: 1.5em; display:inline-block; width: 100%;">{{ props.row.task.split('\n')[0] }}</div>
                        <div v-if="props.row.task.includes('\n')" style="font-size: 1em; display:inline-block; width: 100%;">{{ props.row.task.split('\n').slice(1).join('\n') }}</div>
                    </div>
                </q-td>
                """
            )




            table.style("background-color: lightblue;")
            table.on("delete", delete)
            table.on("change_status", change_status)


    def chat(self):

        with ui.row().style("width: 60vw; border: solid black 1px; margin-left: 20%; margin-right: 20%; height: 60vh; background-color: lightblue;"):
            ui.chat_message(["Yooo! What's up guys! Are y'all going to see the Eclipse?\n"], name="Bob", stamp="1:30", avatar="https://cdn.quasar.dev/img/avatar1.jpg")
            ui.separator().style("background-color: lightblue;")  # Add some vertical spacing between messages
            ui.chat_message(["Probably not. I have to finish some stupid 1XD3 exam "], name="Janice", stamp="2:15", avatar="https://cdn.quasar.dev/img/avatar2.jpg")
            ui.separator().style("background-color: lightblue;")  # Add some vertical spacing between messages
            with ui.row().style("width: 100%; justify-content: right; margin-right: 2%;"):
                ui.chat_message(["I'll be in the field behind the stadium!"], sent=True, name="me", avatar="https://cdn.quasar.dev/img/avatar4.jpg")
            ui.separator().style("background-color: white; height: 5%; margin-top: 35%;")
        with ui.row().style("width: 60vw; margin-left: 20%; margin-right: 20%; background-color: lightblue; border: solid black 1px; padding-left: 3%;"):
                ui.button(icon="add", color="lightblue").style(" width: 5%; height: 100%; margin-top: 1%; ")
                ui.button(icon="image", color="lightblue").style("width: 5%; height: 100%; margin-top: 1%; ")

                ui.input("Type your message here").style("width: 70%; background-color: lightblue")
                ui.button(icon="mood", color="lightblue").style("width: 5%; height: 100%; margin-top: 1%;")


    def progress(self):
        random_compiles = 2542
        percentages = [0.43, 0.16, 0.31]
        tasks_complete = 113
        tasks_percentages = [0.2, 0.4, 0.4]
        # tasks_weekly = [[10], [20], [10], [10], [20], [20], [50], [20], [10], [30]]
        tasks_weekly = [10, 20, 10, 10, 20, 20, 50, 20, 10, 30]
        weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        names = ['Joe', 'Bob', 'Janice']
        with ui.row().style("width: 35vw; height: 40vh; background-color: lightgray; border: 1px solid black; justify-content: center; align-items: center; text-align: center; "):
            ui.label("    Compiles: " + str(random_compiles)).style("font-size: 1.5em; margin: 0; padding: 0px; border: 1px solid black; background-color: lightblue; width: 100%; margin-top: -1%; height: 15%; ")
            with ui.matplotlib(figsize=(3.5, 3.1)).figure as fig:
                    fig.patch.set_facecolor('lightgray')  # Set the background color

                    ax = fig.gca()
                    ax.pie(percentages, labels=names)
        with ui.row().style("width: 50vw; height: 40vh; background-color: lightgray; border: 1px solid black; text-align: center; justify-content: center; align-items: center;"):
            ui.label("Tasks Complete: " + str(tasks_complete)).style("font-size: 1.5em; margin: 0; padding: 0px; border: 1px solid black; background-color: lightblue; width: 100%; margin-top: -1%; height: 15%; ")
            with ui.matplotlib(figsize=(3.5, 3.1)).figure as fig:
                fig.patch.set_facecolor('lightgray')
                ax = fig.gca()
                ax.pie(tasks_percentages, labels=names)


            with ui.line_plot(n=1, limit=10, figsize=(3.5, 3.1), update_every=1).with_legend(['Tasks Completed']) as line_plot:
                for i in range(9):
                    line_plot.push([weeks[i]], [[tasks_weekly[i]]])
            line_plot.style("background-color: lightgray;")

    def index(self):
        self.header
        with ui.row().style("width: 90vw; margin-left: 1vw;"):
            ui.label(f"{self.route}").style("font-size: 2em; margin: 0; padding: 0 15px; border: 1px solid black; background-color: lightgray; ")

        with ui.row().style("width: 90vw; margin-left: 1vw;"):
            with ui.tabs().classes('w-full') as tabs:
                tasks = ui.tab("Tasks").style("width: 25%").style("background-color: #0D99FF;")
                issues = ui.tab("Issues").style("width: 25%").style("background-color: lightblue;")
                chat = ui.tab("Chat").style("width: 25%").style("background-color: lightblue;")
                progress = ui.tab("Progress").style ("width: 25%").style("background-color: lightblue;")
            def func(e):
                if e.value == "Tasks":
                    tasks.style("background-color: #0D99FF;")
                    issues.style("background-color: lightblue;")
                    chat.style("background-color: lightblue;")
                    progress.style("background-color: lightblue;")
                elif e.value == "Issues":
                    issues.style("background-color: #0D99FF;")
                    tasks.style("background-color: lightblue;")
                    chat.style("background-color: lightblue;")
                    progress.style("background-color: lightblue;")
                elif e.value == "Chat":
                    chat.style("background-color: #0D99FF;")
                    tasks.style("background-color: lightblue;")
                    issues.style("background-color: lightblue;")
                    progress.style("background-color: lightblue;")

                elif e.value == "Progress":
                    progress.style("background-color: #0D99FF;")
                    tasks.style("background-color: lightblue;")
                    issues.style("background-color: lightblue;")
                    chat.style("background-color: lightblue;")
                
            with ui.tab_panels(tabs, value=tasks, on_change=lambda e: func(e)).classes('w-full') as tab_panels:
                
                with ui.tab_panel(tasks):
                    with ui.row().style("width: 100%"):
                        # ui.label("Tasks")
                        self.tasks()
                with ui.tab_panel(issues):
                    with ui.row().style("width: 100%"):
                        # ui.label("Tasks")
                        self.issues()

                with ui.tab_panel(chat):
                    with ui.row().style("width: 100%"):
                        # ui.label("Tasks")
                        self.chat()
                with ui.tab_panel(progress):
                    with ui.row().style("width: 100%"):
                        # ui.label("Tasks")
                        self.progress()
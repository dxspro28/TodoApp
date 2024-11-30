import flet as ft

from views.AddTask import AddTask
from views.TaskList import TaskList

def main(page: ft.Page):

    page.window.width = 400
    page.window.height = 400

    def on_route_change(e):
        page.views.append(TaskList(page))
        match page.route:
            case '/add-task':
                page.views.append(AddTask(page))
            case x:
                pass
        page.update()

    page.on_route_change = on_route_change
    page.go('/')
    
ft.app(main)

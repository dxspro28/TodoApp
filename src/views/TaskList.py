import flet as ft

import database.tasks

class TaskList(ft.View):
    def __init__(self, page: ft.Page):
        
        self.appBar = ft.AppBar(
            title=ft.Text('Tareas'),
            leading=ft.Text(' '),
            leading_width=0,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.Icons.ADD, on_click=lambda _: page.go('/add-task')),
                ft.IconButton(ft.Icons.DELETE, on_click=self.show_confirmation),
                ft.IconButton(ft.Icons.CHECK_BOX, on_click=self.mark_all_as_done)
            ],
        )

        db = database.tasks.Tasks('tareas.db')
        tasks = db.get_tasks()

        self.task_list = ft.ListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(task[1]),
                    subtitle=ft.Text(task[2]),
                    trailing=ft.Checkbox(value=bool(task[3]), on_change=self.on_checkbox_change, data=(int(task[0]), task[1], task[2]))
                ) for task in tasks
            ],
            expand=True,  # Allow the list view to expand
        )

        controls = [
            self.appBar,
            self.task_list
        ]

        super().__init__(
            '/',
            controls,
        )
    
    def show_message(self, msg, bc=ft.Colors.GREY_400, fc='black'):
        self.page.snack_bar = ft.SnackBar(
                ft.Text(msg, color=fc, weight='bold'),
                bgcolor=bc,
                open=True
            )
        self.page.update()

    def on_checkbox_change(self, e):
        db = database.tasks.Tasks('tareas.db')
        (ident, title, desc) = e.control.data
        done = e.control.value
        db.update_task(ident, title, desc, done)

    
    def delete_completed_tasks(self, _):
        db = database.tasks.Tasks('tareas.db')
        count = 0
        for task in db.get_tasks():
            if task[3]:
                db.delete_task(task[0])
                count += 1
            
        self.task_list.controls = [
            ft.ListTile(
                title=ft.Text(task[1]),
                subtitle=ft.Text(task[2]),
                trailing=ft.Checkbox(value=bool(task[3]), on_change=self.on_checkbox_change, data=(int(task[0]), task[1], task[2]))
            ) for task in db.get_tasks() if not task[3]
        ]
        self.task_list.update()
        if count > 1:
            self.show_message(f'Fueron eliminadas {count} tareas', bc='blue', fc='white')
        elif count == 1:
            self.show_message(f'Fue eliminada 1 tarea', bc='blue', fc='white')
        else:
            self.show_message('No hay tareas completadas', bc='blue', fc='white')

    def show_confirmation(self, e):
        def delete_and_close(e=None):
            self.delete_completed_tasks(None)
            self.page.close_dialog()

        dialog = ft.AlertDialog(
            title=ft.Text('Confirmar'),
            content=ft.Text('¿Está seguro de que desea eliminar las tareas completadas?'),
            actions=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton('Aceptar', on_click=delete_and_close),
                        ft.ElevatedButton('Cancelar', on_click=lambda _: self.page.close_dialog()),
                    ],
                    alignment=ft.CrossAxisAlignment.END
                )
            ]
        )
        self.page.show_dialog(dialog)

    def mark_all_as_done(self, e=None):
        db = database.tasks.Tasks('tareas.db')
        tasks = db.get_tasks()
        for task in tasks:
            db.update_task(task[0], task[1], task[2], True)
        self.task_list.controls = [
            ft.ListTile(
                title=ft.Text(task[1]),
                subtitle=ft.Text(task[2]),
                trailing=ft.Checkbox(value=bool(task[3]), on_change=self.on_checkbox_change, data=(int(task[0]), task[1], task[2]))
            ) for task in db.get_tasks()
        ]
        self.task_list.update()

import flet as ft
import database.tasks

class AddTask(ft.View):
    def __init__(self, page: ft.Page):

        self.page = page

        # barra superior
        self.appbar = ft.AppBar(
            title=ft.Text("Añadir tarea"),
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go('/')),
            # color=ft.colors.SURFACE_VARIANT,
            bgcolor=ft.colors.SURFACE_VARIANT,
            elevation=1,
        )

        # inputs para los datos
        self.title = ft.TextField(
            label='Título',
            width=ft.CrossAxisAlignment.STRETCH,
            max_lines=1,
            on_submit=lambda _: self.description.focus(),
            expand=True,
        )
        self.description = ft.TextField(
            label='Descripción',
            width=ft.CrossAxisAlignment.STRETCH,
            max_lines=10,
            on_submit=lambda _: self.submit(),
            expand=True,
        )
        self.btnSubmit = ft.ElevatedButton(
            'Guardar', ft.Icons.SAVE, on_click=self.submit,
            width='90%', expand=True, bgcolor=ft.Colors.GREY_200, color=ft.Colors.BLUE_600
            )
        
        controls = [
            self.appbar,
            ft.Column(
                controls=[
                    ft.Row([self.title]),
                    ft.Row([self.description]),
                    ft.Divider(),
                    ft.Row([self.btnSubmit,])
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]

        super().__init__(
            '/add-task',
            controls
        )
    
    def show_message(self, msg, bc=ft.Colors.GREY_400, fc='black'):
        self.page.snack_bar = ft.SnackBar(
                ft.Text(msg, color=fc, weight='bold'),
                bgcolor=bc,
                open=True
            )
        self.page.update()

    def submit(self, e=None):
        if not self.title.value:
            self.show_message('Ingresa un título', bc='red', fc='white')
            return
        
        if not self.description.value:
            self.show_message('Ingrese una descripción', bc='red', fc='white')
            return
        
        
        db = database.tasks.Tasks('tareas.db')
        db.add_task(title=self.title.value, description=self.description.value, completed=False)
        
        self.page.snack_bar = ft.SnackBar(
            ft.Text('Tarea agregada', color='white', weight='bold'),
            bgcolor='green',
            open=True
        )
        self.page.go('/')
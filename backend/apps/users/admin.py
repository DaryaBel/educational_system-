from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Employee, StudentSubject, User, Student, Subject
from users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, которые используются при отображении модели пользователя.
    # Они переопределяют определения в базовом UserAdmin
    # которые ссылаются на определенные поля в auth.User.list_display = ['full_name', 'email']
    list_display = ['full_name', 'email']
    fieldsets = [
        ['Данные авторизации', {'fields': ['email', 'password']}],
        ['Личная информация', {'fields': ['last_name', 'first_name']}],
        ['Настройки', {'fields': ['groups', 'is_admin', 'is_active', 'is_staff', 'is_superuser']}],
        ['Важные отметки времени', {'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets не является стандартным атрибутом ModelAdmin. UserAdmin
    # переопределяет get_fieldsets для использования этого атрибута при создании пользователя.
    add_fieldsets = [[None, {'classes': ['wide'], 'fields': [
        'email', 'first_name', 'last_name', 'password1', 'password2']}], ]
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login', 'registered_at']


class StudentSubjectInline(admin.StackedInline):
    model = StudentSubject
    extra = 0
    
class EmployeeAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('__str__', 'organization', 'moderated',)
    search_fields = ('user', 'organization', 'position',)
    list_filter = ('moderated',)
    actions = ["moderate"]
    
    def moderate(self, request, queryset):
        # Подтвердить аккаунт
        row_update = queryset.update(moderated=True)
        message_bit = f"Количество пользователей, аккаунты которых были успешно подтверждены: {row_update}"
        self.message_user(request, f"{message_bit}")

    moderate.short_description = "Подтвердить аккаунт"
    moderate.allowed_permissions = ('change', )

class StudentAdmin(admin.ModelAdmin):
    """Школьники"""
    list_display = ('__str__', 'birthdate',)
    search_fields = ('user', 'patronymic',)
    inlines = [StudentSubjectInline]

class SubjectAdmin(admin.ModelAdmin):
    """Предметы"""
    list_display = ('__str__',)
    search_fields = ('name',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

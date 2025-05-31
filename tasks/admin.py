from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # リスト表示の設定
    list_display = ('title', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
    
    # 詳細画面の設定
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'description')
        }),
        ('ステータス', {
            'fields': ('completed',)
        }),
        ('タイムスタンプ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    
    # アクション
    actions = ['mark_as_completed', 'mark_as_pending']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated}個のタスクを完了済みにしました。')
    mark_as_completed.short_description = '選択されたタスクを完了済みにする'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated}個のタスクを進行中にしました。')
    mark_as_pending.short_description = '選択されたタスクを進行中にする'

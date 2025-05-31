from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.utils import timezone
import re

register = template.Library()

@register.filter
def task_status_badge(task):
    """タスクのステータスバッジを生成"""
    if task.completed:
        return format_html(
            '<span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>完了</span>'
        )
    else:
        return format_html(
            '<span class="badge bg-warning text-dark"><i class="bi bi-clock me-1"></i>進行中</span>'
        )

@register.filter
def time_since_japanese(value):
    """日本語での経過時間表示"""
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.days > 7:
        return value.strftime('%Y年%m月%d日')
    elif diff.days > 0:
        return f'{diff.days}日前'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours}時間前'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes}分前'
    else:
        return 'たった今'

@register.filter
def progress_color(percentage):
    """進捗率に応じた色を返す"""
    if percentage >= 80:
        return 'bg-success'
    elif percentage >= 50:
        return 'bg-info'
    elif percentage >= 20:
        return 'bg-warning'
    else:
        return 'bg-danger'

@register.inclusion_tag('tasks/task_card.html')
def task_card(task):
    """タスクカードコンポーネント"""
    return {'task': task}

@register.simple_tag
def task_priority_icon(task):
    """タスクの優先度アイコン（タイトルの長さで判定）"""
    if not task.title:
        return ""
    
    title_length = len(task.title)
    if title_length > 50:
        return mark_safe('<i class="bi bi-exclamation-triangle text-danger" title="長いタイトル"></i>')
    elif '緊急' in task.title or '急' in task.title:
        return mark_safe('<i class="bi bi-lightning text-warning" title="緊急"></i>')
    elif '重要' in task.title:
        return mark_safe('<i class="bi bi-star text-info" title="重要"></i>')
    else:
        return ""

@register.simple_tag
def completion_message(completed_count, total_count):
    """完了メッセージ"""
    if total_count == 0:
        return "タスクを追加してみましょう！"
    
    percentage = (completed_count / total_count) * 100
    
    if percentage == 100:
        return "🎉 すべてのタスクが完了しています！素晴らしいです！"
    elif percentage >= 80:
        return "🔥 もう少しで完了です！頑張って！"
    elif percentage >= 50:
        return "💪 順調に進んでいます！"
    elif percentage >= 20:
        return "📈 良いスタートを切っています！"
    else:
        return "🚀 今日も頑張りましょう！"

@register.filter
def highlight_keywords(text, keywords="重要,緊急,優先"):
    """キーワードをハイライト"""
    if not text:
        return text
    
    keyword_list = keywords.split(',')
    result = text
    
    for keyword in keyword_list:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        result = pattern.sub(
            f'<mark class="bg-warning">{keyword}</mark>',
            result
        )
    
    return mark_safe(result) 
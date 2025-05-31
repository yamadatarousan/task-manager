from django import forms
from .models import Task
import re

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タスクのタイトルを入力してください',
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'タスクの詳細説明を入力してください（任意）',
                'rows': 3
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'タイトル',
            'description': '説明',
            'completed': '完了済み'
        }
    
    def clean_title(self):
        """タイトルのカスタムバリデーション"""
        title = self.cleaned_data.get('title')
        
        if not title:
            raise forms.ValidationError('タイトルは必須です。')
        
        # 文字数チェック
        if len(title.strip()) < 3:
            raise forms.ValidationError('タイトルは3文字以上で入力してください。')
        
        # 禁止文字チェック
        forbidden_chars = ['<', '>', '&', '"', "'"]
        for char in forbidden_chars:
            if char in title:
                raise forms.ValidationError(f'タイトルに「{char}」は使用できません。')
        
        # 重複チェック（編集時は除外）
        existing_task = Task.objects.filter(title__iexact=title.strip())
        if self.instance.pk:
            existing_task = existing_task.exclude(pk=self.instance.pk)
        
        if existing_task.exists():
            raise forms.ValidationError('同じタイトルのタスクが既に存在します。')
        
        return title.strip()
    
    def clean_description(self):
        """説明のカスタムバリデーション"""
        description = self.cleaned_data.get('description')
        
        if description:
            # 文字数制限
            if len(description) > 1000:
                raise forms.ValidationError('説明は1000文字以内で入力してください。')
            
            # URLや悪意のあるコンテンツのチェック
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            if re.search(url_pattern, description):
                raise forms.ValidationError('URLの記載は許可されていません。')
        
        return description
    
    def clean(self):
        """フォーム全体のバリデーション"""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        
        # タイトルと説明が同じ場合のチェック
        if title and description and title.lower() == description.lower():
            raise forms.ValidationError('タイトルと説明を同じにすることはできません。')
        
        return cleaned_data
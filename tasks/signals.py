from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
import logging

# ログ設定
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    """タスク作成・更新後の処理"""
    if created:
        # 新規作成時
        logger.info(f'新しいタスクが作成されました: {instance.title}')
        print(f'📝 新しいタスク「{instance.title}」が作成されました！')
        
        # タスク番号を設定（IDベース）
        if not instance.title.startswith('#'):
            instance.title = f'#{instance.id:04d} {instance.title}'
            # save()を呼ぶとシグナルが再度発火するので、update()を使用
            Task.objects.filter(id=instance.id).update(title=instance.title)
    else:
        # 更新時
        logger.info(f'タスクが更新されました: {instance.title}')
        print(f'✏️ タスク「{instance.title}」が更新されました')

@receiver(post_delete, sender=Task)
def task_post_delete(sender, instance, **kwargs):
    """タスク削除後の処理"""
    logger.info(f'タスクが削除されました: {instance.title}')
    print(f'🗑️ タスク「{instance.title}」が削除されました')

@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance, **kwargs):
    """タスク保存前の処理"""
    if instance.pk:
        # 既存タスクの場合、ステータス変更をチェック
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            if old_instance.completed != instance.completed:
                if instance.completed:
                    logger.info(f'タスクが完了されました: {instance.title}')
                    print(f'✅ おめでとうございます！「{instance.title}」が完了しました！')
                else:
                    logger.info(f'タスクが未完了に戻されました: {instance.title}')
                    print(f'🔄 「{instance.title}」が進行中に戻されました')
        except Task.DoesNotExist:
            pass 
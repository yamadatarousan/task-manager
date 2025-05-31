from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'タスクの統計情報を表示します'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='指定した日数前からの統計を表示 (デフォルト: 7日)'
        )
        parser.add_argument(
            '--export',
            action='store_true',
            help='統計情報をCSVファイルに出力'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        export = options['export']
        
        # 指定期間の計算
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # 統計データの取得
        all_tasks = Task.objects.all()
        period_tasks = all_tasks.filter(created_at__gte=start_date)
        
        total_count = all_tasks.count()
        period_count = period_tasks.count()
        completed_count = all_tasks.filter(completed=True).count()
        pending_count = all_tasks.filter(completed=False).count()
        period_completed = period_tasks.filter(completed=True).count()
        
        # 完了率の計算
        completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # 結果の表示
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'📊 タスク統計情報 (過去{days}日間)'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        self.stdout.write(f'📈 全体統計:')
        self.stdout.write(f'  総タスク数: {total_count}')
        self.stdout.write(f'  完了済み: {completed_count}')
        self.stdout.write(f'  進行中: {pending_count}')
        self.stdout.write(f'  完了率: {completion_rate:.1f}%')
        
        self.stdout.write(f'\n📅 期間統計 (過去{days}日間):')
        self.stdout.write(f'  新規作成: {period_count}')
        self.stdout.write(f'  期間内完了: {period_completed}')
        
        # 日別統計
        self.stdout.write(f'\n📊 日別作成数:')
        for i in range(days):
            day = end_date - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            day_count = all_tasks.filter(
                created_at__gte=day_start,
                created_at__lt=day_end
            ).count()
            self.stdout.write(f'  {day.strftime("%Y-%m-%d")}: {day_count}個')
        
        # 最新のタスク
        recent_tasks = all_tasks.order_by('-created_at')[:5]
        if recent_tasks:
            self.stdout.write(f'\n📝 最新のタスク (上位5件):')
            for i, task in enumerate(recent_tasks, 1):
                status = '✅' if task.completed else '⏳'
                self.stdout.write(f'  {i}. {status} {task.title}')
        
        # CSVエクスポート
        if export:
            self.export_to_csv(all_tasks)
        
        self.stdout.write(self.style.SUCCESS('\n✨ 統計情報の表示が完了しました'))
    
    def export_to_csv(self, tasks):
        """統計情報をCSVファイルに出力"""
        import csv
        from django.conf import settings
        import os
        
        filename = f'task_stats_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join(settings.BASE_DIR, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'タイトル', 'ステータス', '作成日', '更新日'])
            
            for task in tasks:
                writer.writerow([
                    task.id,
                    task.title,
                    '完了' if task.completed else '進行中',
                    task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
        
        self.stdout.write(
            self.style.SUCCESS(f'📁 CSVファイルを出力しました: {filename}')
        ) 
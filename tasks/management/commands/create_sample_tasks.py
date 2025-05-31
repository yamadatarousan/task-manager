from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = 'サンプルタスクを作成します'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='作成するタスク数 (デフォルト: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='既存のタスクを削除してから作成'
        )
    
    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']
        
        if clear:
            deleted_count = Task.objects.count()
            Task.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'既存のタスク{deleted_count}個を削除しました。')
            )
        
        sample_tasks = [
            {
                'title': '重要：プロジェクトの企画書作成',
                'description': 'Q2プロジェクトの企画書を作成し、関係者に共有する',
                'completed': True
            },
            {
                'title': 'チーム会議の準備',
                'description': '来週の定例会議のアジェンダを作成し、資料を準備する',
                'completed': False
            },
            {
                'title': '緊急：バグ修正',
                'description': 'ユーザー登録画面のバリデーションエラーを修正する',
                'completed': False
            },
            {
                'title': 'データベース設計の見直し',
                'description': 'パフォーマンス改善のためのテーブル構造見直し',
                'completed': True
            },
            {
                'title': 'コードレビューの実施',
                'description': '新機能のプルリクエストをレビューする',
                'completed': False
            },
            {
                'title': '重要：クライアント向けデモ準備',
                'description': '来月のクライアントデモ用のプレゼンテーション準備',
                'completed': False
            },
            {
                'title': 'テストケースの作成',
                'description': '新機能に対する自動テストケースを作成する',
                'completed': True
            },
            {
                'title': 'ドキュメントの更新',
                'description': 'API仕様書とユーザーマニュアルの更新',
                'completed': False
            },
            {
                'title': '緊急：セキュリティパッチ適用',
                'description': 'フレームワークのセキュリティアップデート適用',
                'completed': True
            },
            {
                'title': 'パフォーマンステストの実施',
                'description': '負荷テストとボトルネックの特定',
                'completed': False
            }
        ]
        
        created_count = 0
        for i in range(count):
            task_data = sample_tasks[i % len(sample_tasks)]
            task = Task.objects.create(
                title=f"{task_data['title']} #{i+1}",
                description=task_data['description'],
                completed=task_data['completed']
            )
            created_count += 1
            
            # 進捗表示
            if created_count % 5 == 0:
                self.stdout.write(f'作成済み: {created_count}/{count}')
        
        self.stdout.write(
            self.style.SUCCESS(f'✨ {created_count}個のサンプルタスクを作成しました！')
        )
        
        # 統計表示
        total = Task.objects.count()
        completed = Task.objects.filter(completed=True).count()
        pending = Task.objects.filter(completed=False).count()
        
        self.stdout.write('\n📊 現在の統計:')
        self.stdout.write(f'  総タスク数: {total}')
        self.stdout.write(f'  完了済み: {completed}')
        self.stdout.write(f'  進行中: {pending}')
        self.stdout.write(f'  完了率: {(completed/total*100):.1f}%')
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ サンプルデータの作成が完了しました！')
        ) 
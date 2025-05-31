# 📋 Django Task Manager

Djangoフレームワークの主要機能を活用した高機能タスク管理アプリケーションです。Bootstrap 5による美しいUIと、Djangoの様々な機能を学習できる実用的なサンプルアプリケーションとして設計されています。

## 🌟 主な機能

### 基本機能
- ✅ タスクの作成・編集・削除
- 📊 統計ダッシュボード（完了率・進捗表示）
- 🏷️ タスクステータス管理（進行中/完了）
- 📱 レスポンシブデザイン（Bootstrap 5）

### 高度なDjango機能
- 🔧 **Django Admin** - 管理画面でのタスク管理
- ✨ **カスタムバリデーション** - 堅牢なフォーム検証
- 🎯 **Django Signals** - 自動処理とログ記録
- 📈 **Management Commands** - コマンドライン管理ツール
- 🏷️ **カスタムテンプレートタグ** - 再利用可能なUI コンポーネント

## 🚀 セットアップ

### 前提条件
- Python 3.8以上
- Django 3.2以上

### インストール
```bash
# リポジトリのクローン
git clone <repository-url>
cd task-manager

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install django

# データベースの初期化
python manage.py migrate

# 管理者ユーザーの作成
python manage.py createsuperuser

# サンプルデータの作成（オプション）
python manage.py create_sample_tasks --count 15

# 開発サーバーの起動
python manage.py runserver 8001
```

### アクセス
- **メインアプリ**: http://127.0.0.1:8001/
- **Django Admin**: http://127.0.0.1:8001/admin/

## 🔧 Djangoフレームワーク活用機能

### 1. Django Admin（管理画面）
**ファイル**: `tasks/admin.py`

Djangoの自動管理画面機能をカスタマイズして、強力なタスク管理インターface を提供：

```python
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'created_at')
    actions = ['mark_as_completed', 'mark_as_pending']
```

**機能**:
- タスクの一覧表示・検索・フィルタリング
- インライン編集（完了状態の一括変更）
- カスタムアクション（一括ステータス変更）
- フィールドセットによる整理された編集画面

### 2. カスタムバリデーション（フォーム検証）
**ファイル**: `tasks/forms.py`

Djangoのフォームバリデーション機能を活用した堅牢なデータ検証：

```python
def clean_title(self):
    title = self.cleaned_data.get('title')
    if len(title.strip()) < 3:
        raise forms.ValidationError('タイトルは3文字以上で入力してください。')
    return title.strip()
```

**機能**:
- 文字数制限とフォーマット検証
- 禁止文字・URLチェック
- 重複データの防止
- リアルタイムJavaScriptバリデーション

### 3. Django Signals（自動処理）
**ファイル**: `tasks/signals.py`, `tasks/apps.py`

Djangoのシグナル機能を使った自動処理とログ記録：

```python
@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        # タスク番号の自動付与
        instance.title = f'#{instance.id:04d} {instance.title}'
        Task.objects.filter(id=instance.id).update(title=instance.title)
```

**機能**:
- タスク作成時の自動ID番号付与
- ステータス変更時の通知メッセージ
- データベース操作のログ記録
- モデル操作に連動した自動処理

### 4. Management Commands（コマンドライン管理）
**ファイル**: `tasks/management/commands/`

Djangoのカスタムコマンド機能でデータ管理を自動化：

#### 統計情報表示
```bash
# 過去7日間の統計表示
python manage.py task_stats --days 7

# CSVファイルエクスポート
python manage.py task_stats --export
```

#### サンプルデータ作成
```bash
# 10個のサンプルタスク作成
python manage.py create_sample_tasks --count 10

# 既存データクリア後に作成
python manage.py create_sample_tasks --clear --count 20
```

**機能**:
- 詳細な統計レポート生成
- 日別タスク作成数の表示
- CSVデータエクスポート
- テスト用サンプルデータ生成

### 5. カスタムテンプレートタグ（UI拡張）
**ファイル**: `tasks/templatetags/task_extras.py`

Djangoのテンプレートタグ機能で再利用可能なUIコンポーネントを作成：

```python
@register.filter
def time_since_japanese(value):
    # 日本語での経過時間表示
    if diff.days > 0:
        return f'{diff.days}日前'
    return 'たった今'
```

**機能**:
- 日本語経過時間表示（`{{ task.created_at|time_since_japanese }}`）
- 優先度アイコン自動表示（`{% task_priority_icon task %}`）
- キーワードハイライト（`{{ task.title|highlight_keywords }}`）
- 動的完了メッセージ（`{% completion_message completed total %}`）
- 進捗バー色変更（`{{ rate|progress_color }}`）

## 📱 使用方法

### 基本操作
1. **タスク作成**: 「新しいタスク」ボタンから作成
2. **タスク編集**: カード内の「編集」ボタンから
3. **タスク削除**: カード内の「削除」ボタンから
4. **統計確認**: ダッシュボードで進捗を確認

### 高度な機能
1. **管理画面**: `/admin/` にアクセスしてバックエンド管理
2. **一括操作**: 管理画面でタスクを一括選択・変更
3. **データ分析**: `task_stats` コマンドで詳細分析
4. **サンプル生成**: `create_sample_tasks` でテストデータ作成

## 🎨 カスタマイズ

### 優先度キーワード
タイトルに以下のキーワードを含めると、自動で優先度アイコンが表示されます：
- 「重要」→ ⭐ 重要アイコン
- 「緊急」「急」→ ⚡ 緊急アイコン
- 長いタイトル（50文字以上）→ ⚠️ 警告アイコン

### テンプレートタグのカスタマイズ
`tasks/templatetags/task_extras.py` を編集して、独自のフィルターやタグを追加できます。

## 🏗️ アーキテクチャ

```
task-manager/
├── tasks/                          # メインアプリケーション
│   ├── admin.py                   # Django Admin設定
│   ├── forms.py                   # カスタムフォーム・バリデーション
│   ├── models.py                  # データモデル
│   ├── signals.py                 # Django Signals
│   ├── views.py                   # ビューロジック
│   ├── management/commands/       # カスタムコマンド
│   │   ├── task_stats.py         # 統計表示コマンド
│   │   └── create_sample_tasks.py # サンプルデータ作成
│   ├── templatetags/              # カスタムテンプレートタグ
│   │   └── task_extras.py        # UI拡張タグ
│   └── templates/tasks/           # テンプレート
│       ├── task_list.html        # タスク一覧
│       ├── task_form.html        # タスク作成・編集
│       └── task_confirm_delete.html # 削除確認
├── templates/                     # 共通テンプレート
│   └── base.html                 # ベーステンプレート
└── task_manager/                  # プロジェクト設定
    ├── settings.py               # Django設定
    └── urls.py                   # URL設定
```

## 🎓 学習ポイント

このアプリケーションでは以下のDjango機能を実践的に学習できます：

1. **MVC アーキテクチャ**: Model-View-Controller パターンの理解
2. **ORM操作**: データベース操作の抽象化
3. **フォーム処理**: バリデーション・セキュリティ
4. **テンプレート継承**: 再利用可能なHTML構造
5. **管理画面カスタマイズ**: 自動生成画面の拡張
6. **シグナル処理**: イベント駆動プログラミング
7. **コマンド作成**: バッチ処理・メンテナンス
8. **テンプレートタグ**: ビュー層の拡張

## 🔗 技術スタック

- **バックエンド**: Django 3.2+ (Python)
- **フロントエンド**: Bootstrap 5.3 + Bootstrap Icons
- **データベース**: SQLite（開発用）
- **スタイリング**: カスタムCSS + Bootstrap

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 コントリビューション

プルリクエストやイシューの報告を歓迎します。新機能の追加や改善提案もお気軽にどうぞ！

---

**🎯 このアプリケーションは、Djangoフレームワークの包括的な学習を目的として設計されています。実際のWebアプリケーション開発で必要となる様々な機能を、実践的なタスク管理システムを通して学ぶことができます。**

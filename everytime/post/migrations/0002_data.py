from django.db import migrations

def create_default_data(apps, schema_editor):
    Category = apps.get_model('post', 'Category')
    if not Category.objects.filter(title="비밀게시판").exists():
        Category.objects.create(title="비밀게시판", slug="secret")
    if not Category.objects.filter(title="새내기게시판").exists():
        Category.objects.create(title="새내기게시판", slug="freshmen")
    if not Category.objects.filter(title="디지털소프트웨어공학부").exists():
        Category.objects.create(title="디지털소프트웨어공학부", slug="deptofcse")
    if not Category.objects.filter(title="소프트웨어전공").exists():
        Category.objects.create(title="소프트웨어전공", slug="software")
    if not Category.objects.filter(title="파이썬웹프로그래밍").exists():
        Category.objects.create(title="파이썬웹프로그래밍", slug="PWP")

class Migration(migrations.Migration):
    dependencies = [
        ('post', '0001_initial'),  # 이전 마이그레이션 파일 명
    ]

    operations = [
        migrations.RunPython(create_default_data),
    ]

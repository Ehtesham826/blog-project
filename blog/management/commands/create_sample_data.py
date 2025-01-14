from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category, Tag


class Command(BaseCommand):
    help = 'Creates sample categories and tags for the blog'

    def handle(self, *args, **options):
        # Create Categories
        categories = [
            'Technology',
            'Lifestyle',
            'Health',
            'Education',
            'Travel',
            'Food',
            'Sports',
            'Entertainment'
        ]
        
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': slugify(cat_name),
                    'description': f'Posts about {cat_name.lower()}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {cat_name}'))

        # Create Tags
        tags = [
            'python',
            'django',
            'web-development',
            'programming',
            'tutorial',
            'tips',
            'beginner',
            'advanced',
            'ai',
            'machine-learning',
            'healthcare',
            'fitness',
            'cooking',
            'photography',
            'design'
        ]
        
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Tag already exists: {tag_name}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Sample categories and tags created successfully!'))


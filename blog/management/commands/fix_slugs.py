from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category, Tag


class Command(BaseCommand):
    help = 'Fixes empty slugs for categories and tags'

    def handle(self, *args, **options):
        # Fix Category slugs
        categories_fixed = 0
        for category in Category.objects.filter(slug=''):
            category.slug = slugify(category.name)
            category.save()
            categories_fixed += 1
            self.stdout.write(self.style.SUCCESS(f'Fixed category: {category.name} -> {category.slug}'))
        
        # Fix Tag slugs
        tags_fixed = 0
        for tag in Tag.objects.filter(slug=''):
            tag.slug = slugify(tag.name)
            tag.save()
            tags_fixed += 1
            self.stdout.write(self.style.SUCCESS(f'Fixed tag: {tag.name} -> {tag.slug}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Fixed {categories_fixed} categories and {tags_fixed} tags!'))


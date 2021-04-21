from django.db import models
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('설명', max_length=100, blank=True, help_text='Simple description text.')
    content = models.TextField('본문')
    created_dt = models.DateTimeField('생성일', auto_now=True)
    modify_dt = models.DateTimeField('수정일', auto_now=True)
    is_active = models.BooleanField('활성화 여부', default=True)
    deleted_at = models.DateTimeField('삭제일', null=True, blank=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'post'
        db_table = 'blog_posts'
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:post_detail', args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()




from django.db import models

# models
from base.models import BaseModel

# standard library
import re


class Interview(BaseModel):
    def file_path(self, name):
        """ file path for the file obj """
        return "%s" % name

    title = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(
        unique=True, null=True, blank=True,
    )
    summary = models.TextField(
    )
    who_you_are = models.TextField(
    )
    what_hardware = models.TextField(
    )
    what_software = models.TextField(
    )
    dream_setup = models.TextField(
    )
    picture = models.ImageField(
        upload_to=file_path, null=True, blank=True,
    )
    tags = models.ManyToManyField(
        'Tag', related_name='interviews', editable=False,
    )

    image_sizes = [
        (265, 170),
        (530, 340),
    ]

    class Meta:
        ordering = ['-created_at']

    def parse_tags(self, commit=False):
        def tag_replace(match):
            contents = match.group(1)

            tag = Tag.objects.get(title=contents)
            if commit:
                self.tags.add(tag)

            return '[{}]({})'.format(tag.title, tag.link)

        if commit:
            self.tags.remove()

        search = '\[(\w+)!!!\]'

        self.summary = re.sub(search, tag_replace, self.summary)
        self.who_you_are = re.sub(search, tag_replace, self.who_you_are)
        self.what_hardware = re.sub(search, tag_replace, self.what_hardware)
        self.what_software = re.sub(search, tag_replace, self.what_software)
        self.dream_setup = re.sub(search, tag_replace, self.dream_setup)

    #public methods
    def save(self, *args, **kwargs):
        """
        Interview save method, overriden to set the picture size
        """

        super(Interview, self).save(*args, **kwargs)
        try:
            self._process_image('picture')
        except:
            pass

        self.parse_tags(commit=True)


class Category(BaseModel):
    title = models.CharField(
        max_length=255,
    )


class Tag(BaseModel):
    cateogry = models.ForeignKey(
        Category,
    )
    title = models.CharField(
        max_length=255,
    )
    link = models.URLField(
        blank=True, null=True,
    )

    def __unicode__(self):
        return self.title

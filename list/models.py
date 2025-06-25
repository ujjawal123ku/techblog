from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse


def upload_to(instance, filename):
    return f"assets/image/{filename}"


def video_upload_to(instance, filename):
    return f"assets/videos/{filename}"


class Blog(models.Model):
    title = models.CharField(max_length=100, blank=False)  # Increased length for flexibility
    desc = models.CharField(max_length=2000, blank=False)  # Detailed description
    full_article = models.TextField(blank=False)  # For large content
    datetime = models.DateTimeField(auto_now_add=True)
    image = ResizedImageField(upload_to=upload_to, null=True, blank=True)
    video = models.FileField(
        upload_to=video_upload_to,
        null=True,
        blank=True,
    )  # Video field
    category = models.CharField(
        max_length=50,
        choices=[
            ("Tech", "Tech"),
            ("Health", "Health"),
            ("Lifestyle", "Lifestyle"),
            ("Education", "Education"),
            ("Business", "Business"),
            ("Sports", "Sports"),
            ("Opinions", "Opinions"),
            ("Startups", "Startups"),
            ("Technology", "Technology"),
            ("Crime", "Crime"),
            ("World", "World"),
            ("Art", "Art"),
            ("History", "History"),
            ("Culture", "Culture"),
            ("Finance", "Finance"),
            ("Fashion", "Fashion"),
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Environment", "Environment"),
            ("Science", "Science"),
            ("Politics", "Politics"),
            ("Entertainment", "Entertainment"),
            ("Sports", "Sports"),
            ("Other", "Other"),
        ],
        default="Other",
        blank=False,
    )  # Dropdown for categories
    author = models.CharField(max_length=50, blank=True)  # Author name
    reading_time = models.IntegerField(
        null=True, blank=True, help_text="Estimated reading time in minutes"
    )  # Reading time
    keywords = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated keywords for SEO"
    )  # SEO keywords
    is_featured = models.BooleanField(default=False)  # Highlight featured articles

    class Meta:
        ordering = ["-datetime"]

    def __str__(self) -> str:
        return self.title

    def estimate_reading_time(self):
        """
        Estimate reading time based on the full_article length.
        Assuming average reading speed of 200 words per minute.
        """
        word_count = len(self.full_article.split())
        return max(1, word_count // 200)

    def get_shareable_link(self):
        """
        Generates a shareable link for the article.
        Assumes the article has a corresponding detail view with a named URL pattern 'blog-detail'.
        """
        return reverse("blog-detail", kwargs={"pk": self.id})

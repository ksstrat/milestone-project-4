import os
from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Vote, Post, Profile
from django.contrib.auth.models import User


# Image verification
try:
    from PIL import Image, UnidentifiedImageError
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False
    Image = None
    UnidentifiedImageError = Exception

# Allowed image extensions
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'featured_image', 'url')
        widgets = {
            'content': SummernoteWidget(),
            'featured_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_featured_image(self):
        # Validate uploaded image (MIME, extension,Pillow verify)
        f = self.cleaned_data.get('featured_image')
        if not f:
            return f

        ct = getattr(f, 'content_type', '') or ''
        if not ct.startswith('image/'):
            raise ValidationError("Please upload an image file (JPG, PNG, GIF, WEBP).")

        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_EXTS:
            raise ValidationError("Unsupported file type. Allowed: JPG, PNG, GIF, WEBP.")

        if PIL_AVAILABLE:
            try:
                img = Image.open(f)
                img.verify()
            except UnidentifiedImageError:
                raise ValidationError("The uploaded file is not a valid image or is corrupted.")
            finally:
                try:
                    f.seek(0)
                except Exception:
                    pass

        return f

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': SummernoteWidget()
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote_type',)

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
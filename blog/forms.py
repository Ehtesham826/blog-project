from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Tag, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile for new user
            UserProfile.objects.create(user=user)
        return user


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'tags', 'content', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError("Title must be at least 10 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Content must be at least 50 characters long.")
        return content

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image size should not exceed 5MB.")
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(f"Invalid image format. Allowed: {', '.join(valid_extensions)}")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        if len(content) > 1000:
            raise forms.ValidationError("Comment must not exceed 1000 characters.")
        return content


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'website', 'location', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Profile picture size should not exceed 2MB.")
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = picture.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(f"Invalid image format. Allowed: {', '.join(valid_extensions)}")
        return picture

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return profile



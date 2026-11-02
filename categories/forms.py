from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'background_video', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'background_video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_background_video(self):
        video = self.cleaned_data.get('background_video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError('Video file too large. Maximum size is 50MB.')
        return video
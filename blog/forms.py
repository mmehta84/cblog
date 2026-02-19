from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'body', 'excerpt', 'featured_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none text-gray-800 text-lg font-medium',
                'placeholder': 'Enter an engaging title...',
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none text-gray-800 resize-none',
                'rows': 3,
                'placeholder': 'Brief description (auto-generated from body if left blank)',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none text-gray-700',
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none text-gray-700',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'No category'
        self.fields['category'].required = False
        self.fields['tags'].required = False


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'flex-1 px-4 py-2 border border-gray-200 rounded-l-lg focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none',
        })
    )

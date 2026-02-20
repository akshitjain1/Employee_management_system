from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    """Form for users to edit their own profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'nickname', 
            'profile_picture', 'phone', 'bio', 'address', 
            'date_of_birth', 'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'readonly': 'readonly'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nickname (optional)'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself (max 500 characters)',
                'rows': 4
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Address',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency Contact Name'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency Contact Phone'
            }),
        }
        
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (max 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            # Check file type
            if not picture.content_type in ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']:
                raise forms.ValidationError("Only image files are allowed (JPEG, PNG, GIF)")
        return picture
    
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 500:
            raise forms.ValidationError("Bio cannot exceed 500 characters")
        return bio

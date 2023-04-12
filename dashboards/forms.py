from django import forms

class ShapefileForm(forms.Form):
    name = forms.CharField(max_length=255)
    file = forms.FileField()


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))    
    



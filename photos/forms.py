# -*- coding: utf-8 -*-
"""
Created on Sun May 26 17:37:33 2024

@author: icesh
"""

from django import forms

from .models import Photos

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class':'form-control-file'})
            
            }
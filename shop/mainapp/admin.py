from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class NotebookAdminForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red;">Загружайте изображеня с минимальным разрешением {}х{}</span>'.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального')
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="notebook"))
        return super().formfield_for_foreignkey(bd_field, request, **kwargs)


class SmartphoneAdminForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red;">Загружайте изображеня с минимальным разрешением {}х{}</span>'.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального')
        return image

class SmartphoneAdmin(admin.ModelAdmin):
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphone"))
        return super().formfield_for_foreignkey(bd_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Notebook, NotebookAdmin)
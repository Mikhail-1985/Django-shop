from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from django.views.generic import DeleteView, View

from .models import *
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', with_respect_to='notebook'
        )
        context = {
            'categories': categories,
            'products': products,            
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DeleteView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):        
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    #model = Model
    #queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDeatailView(CategoryDetailMixin, DeleteView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        #print(product_slug)
        #print(ct_model)
        customer = Customer.objects.get(user=request.user)
        #print(customer)
        cart = Cart.objects.get(owner=customer, in_order=False)
        #print(cart)
        content_type = ContentType.objects.get(model=ct_model)
        #print(content_type)
        product = content_type.model_class().objects.get(slug=product_slug)
        #print(product)
        cart_product = CartProduct.objects.create(
            user=cart.owner, cart=cart, content_object=product, final_price=product.price
        )
        print(product)
        cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)
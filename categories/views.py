from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category
from .forms import CategoryForm

def category_list(request):
    """Display all active categories"""
    categories = Category.objects.filter(is_active=True)
    paginator = Paginator(categories, 12)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    return render(request, 'categories/list.html', {'categories': categories})

def category_detail(request, pk):
    """Display category details with background video"""
    category = get_object_or_404(Category, pk=pk, is_active=True)
    events = category.event_set.filter(is_active=True)[:6]
    return render(request, 'categories/detail.html', {
        'category': category,
        'events': events
    })

@login_required
def category_create(request):
    """Create new category (hosts only)"""
    if not request.user.is_host():
        messages.error(request, 'Only hosts can create categories.')
        return redirect('categories:list')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.host = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('categories:detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'categories/form.html', {'form': form, 'title': 'Create Category'})

@login_required
def category_edit(request, pk):
    """Edit existing category (host only)"""
    category = get_object_or_404(Category, pk=pk)
    if category.host != request.user:
        messages.error(request, 'You can only edit your own categories.')
        return redirect('categories:detail', pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories:detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request, pk):
    """Delete category (host only)"""
    category = get_object_or_404(Category, pk=pk)
    if category.host != request.user:
        messages.error(request, 'You can only delete your own categories.')
        return redirect('categories:detail', pk=pk)
    
    if request.method == 'POST':
        category.is_active = False
        category.save()
        messages.success(request, 'Category deleted successfully!')
        return redirect('categories:list')
    return render(request, 'categories/delete.html', {'category': category})
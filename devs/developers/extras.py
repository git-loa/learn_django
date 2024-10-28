from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateObject(request, object_list, items_per_page=3):
    
    page = request.GET.get('page')
    paginator = Paginator(object_list, items_per_page)
    
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        object_list = paginator.page(page)
    except EmptyPage:
        page =paginator.num_pages
        object_list = paginator.page(page)
    
    leftIndex = int(page)-4
    if leftIndex < 1:
        leftIndex = 1
        
    rightIndex = int(page)+6
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
      
        
    custom_range = range(leftIndex, rightIndex)
    return custom_range, object_list

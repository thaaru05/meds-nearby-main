from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def direction(request):
    #print(request.POST)
    from_way={'lon':request.POST['frm_lon'],'lat':request.POST['frm_lat']}
    to_way={'lon':request.POST['to_lon'],'lat':request.POST['to_lat']}
    data={'from_':from_way,'to_':to_way}
    print(data)
    return render(request,'map/route.html',data)
   
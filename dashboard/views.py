from django.shortcuts import render
from django.views import View

from cmain.views import CMain

# Create your views here.
class DashboardView(View, CMain):
    def get(self, request):
        cmain_context = self.getBasicDetails(request)

        CMain.SITE_DATA.update(cmain_context)
        return render(request, 'home.html', cmain_context)


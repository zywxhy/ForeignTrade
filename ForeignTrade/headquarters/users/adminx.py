import xadmin
from xadmin.plugins.auth import UserAdmin
from users.models import Company,MyUser
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '润州光电'
    site_footer = '润州加油'
    menu_style = 'accordion'




class CompanyAdmin(object):
    model_icon = 'fa fa-group'

    list_display = ['name','remark']
    search_fields =['name','remark']



class MyUserAdmin(object):
    model_icon = 'fa fa-user'

    list_display = ['first_name','company','language','type','is_warehouse_reviewer','is_position_reviewer']
    search_fields = ['first_name','company','language','type','is_warehouse_reviewer','is_position_reviewer']
    list_filter = ['first_name','company','language','type','is_warehouse_reviewer','is_position_reviewer']


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

xadmin.site.unregister(MyUser)
xadmin.site.register(Company,CompanyAdmin)
xadmin.site.register(MyUser,MyUserAdmin)


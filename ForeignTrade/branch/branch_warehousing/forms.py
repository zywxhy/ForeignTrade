from django import forms
from .models import BranchWarehousing



class BranchWarehousingModelForm(forms.ModelForm):
    def __init__(self,initial_dict=None,*args,**kwargs):
        super().__init__(*args,**kwargs)




        self.initial_dict = initial_dict
        if initial_dict is not None:
            for key,value in self.fields.items():
                try:
                    value.initial = initial_dict[key]
                except Exception as e:
                    print(e)
                    continue



    class Meta:
        model = BranchWarehousing
        fields = '__all__'


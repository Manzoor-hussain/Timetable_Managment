from rest_framework import serializers
from superadmin.models import  Allcourse, Allstudent, Constraint
from datetime import date,  timedelta, datetime, time
import pdb

'''
    it is serializer class which convert complex python object into json format
    it is also used for validation purpose.
'''

class UserSerializerForTimeTable(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    class Meta:
        model = Allcourse
        fields = '__all__'
    def get_start_time(self, obj):
        return time(obj.start_time.hour, obj.start_time.minute)

    def get_end_time(self, obj):
        return time(obj.end_time.hour, obj.end_time.minute)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_ = self.context['request'].user
       
     
        DAYS_OF_WEEK = (
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SUN', 'Sunday'),
        )
        day_value=instance.day
        for day in DAYS_OF_WEEK:
          if day[0] == day_value:
              day_value=day[1]
              break
       
        day_value = day_value.upper()
        const_obj=''
        const_obj = Constraint.objects.filter(user=user_, day=day_value).values('user','day','name','start_time','end_time').distinct()

       
        mylist=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SUNDAY']
       
        if const_obj.exists:
            dict_list = list(const_obj.values())
            if day_value in mylist:
                ret['const_obj'] = dict_list
                mylist.remove(day_value)
               
        
                
            return ret

        
       
      




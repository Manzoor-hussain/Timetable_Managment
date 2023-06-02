from rest_framework import serializers
from superadmin.models import  Allcourse, Allstudent, Constraint
from datetime import date,  timedelta,datetime

class UserSerializerForTimeTable(serializers.ModelSerializer):
    class Meta:
        model = Allcourse
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_ = self.context['request'].user
        is_active = False
        lot_size = 0
        user_instrument = ''
        DAYS_OF_WEEK = (
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday'),
            ('SUN', 'Sunday'),
        )
        day_value=instance.day
        for day in DAYS_OF_WEEK:
          if day[0] == day_value:
              day_value=day[1]
              break
       
        day_value = day_value.upper()
       
        const_name = ''
        start_time_con = ''
        end_time_con = ''
        cons_day = ''
        ubi = Constraint.objects.filter(user=user_ ,day=day_value).last()
        const_obj=''
        const_obj = Constraint.objects.filter(user=user_, day=day_value).values('user','day','name','start_time','end_time').distinct()

       
        mylist=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SUNDAY']
       
        if const_obj.exists:
            dict_list = list(const_obj.values())
            if day_value in mylist:
                ret['const_obj'] = dict_list
                mylist.remove(day_value)
               
        
                
            return ret

        
       
      




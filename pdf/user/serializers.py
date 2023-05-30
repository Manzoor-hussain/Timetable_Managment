from rest_framework import serializers
from .models import Pdf, Storefile
from superadmin.models import Myservice, Countservices, Course,Timetable, Allcourse, Allstudent, Constraint
from datetime import date,  timedelta,datetime
import pdb




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
        #ubi = Constraint.objects.values('day').distinct()
       
       
        if ubi:
            is_active = True
          
            const_name = ubi.name
            start_time_con = ubi.start_time
            end_time_con = ubi.end_time
            cons_day =instance.day


       
           
        ret['const_name'] = const_name
        ret['start_time_con'] = start_time_con
        ret['end_time_con'] = end_time_con
        ret['cons_day'] = cons_day
        return ret
        




class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = '__all__'

class StorefileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storefile
        fields = '__all__'
class UserSerializerForCount(serializers.ModelSerializer):
    class Meta:
        model = Myservice
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_ = self.context['request'].user
       
        is_active = False
        count = ''
        created_at =''
       

        ubi = Countservices.objects.filter(user=user_, service=instance).last()
        if ubi:
            count = ubi.count
            created_at =ubi.created_at
            date_format = "%B, %d, %Y, %I:%M %p"           
            formatted_date = created_at.strftime('%Y-%m-%d')
            hour = created_at.hour
            minute = created_at.minute
            second = created_at.second
            time=f"Time: {hour}:{minute:02d}:{second:02d}"
            current_time = datetime.now()
            formatted_today = current_time.strftime("%Y-%m-%d")
            date_object = datetime.strptime(formatted_date, '%Y-%m-%d').date()
            today_object = datetime.strptime(formatted_today, '%Y-%m-%d').date()

            # Calculate the time difference between the two dates
            time_difference = today_object - date_object
            
            if formatted_date == formatted_today:
                ret['created_at'] = "Today"
            elif time_difference.days == 1:
                ret['created_at'] = "Yesterday"
            else:
                ret['created_at'] = formatted_date
            ret['time'] = time

           

       
        
      

        # Compare the date with today and yesterday
       
           
        ret['count'] = count
      
        #   ret['time'] = time
     
        return ret

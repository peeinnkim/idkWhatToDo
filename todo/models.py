from django.db import models
from django.utils import timezone, dateformat

# user class
class UserInfo(models.Model):

    user_no = models.BigAutoField(primary_key=True, verbose_name='NO')
    user_id = models.CharField(max_length=25, blank=False, verbose_name='ID')
    password = models.CharField(max_length=25, blank=False, verbose_name='PWD')
    name = models.CharField(max_length=25, verbose_name='NAME')
    birthday = models.DateField(max_length=25, verbose_name='B-DAY')
    mail = models.CharField(max_length=25, verbose_name='E-MAIL')
    regist_date = models.CharField(max_length=25, default=dateformat.format(timezone.now(), 'Y-m-d'), verbose_name='REG_DATE')
    withdrawal_date = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return "\nno={}, id={}, pwd={}, name={}, b-day={}, mail={}, reg_date={}, wit_date={}\n".format(self.user_no,self.user_id, self.password, self.name, self.birthday, self.mail, self.regist_date, self.withdrawal_date)


# todo class
class Todo(models.Model):

    todo_no = models.BigAutoField(primary_key=True, verbose_name='NO')
    content = models.CharField(max_length=255, verbose_name='CONTENT')
    date = models.CharField(max_length=25, default=dateformat.format(timezone.now(), 'Y-m-d'), verbose_name='DATE')
    is_done = models.BooleanField(default=False, verbose_name='IS_DONE')
    user_no = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='USER_NO')


    def __str__(self):
        return "\ncontent={}, date={}, is_done={}, user_no={}\n".format(self.content, self.date, self.is_done, self.user_no)


    def change_state(self):
        self.is_done = True
        self.save()


# 나중에 regex 만들게
# hashtag_validator = models.Charfield(validators=[validate_hash])
#
# from django.core.exceptions import ValidationError
# import re
#
# def validate_hash(value):
#     reg = re.compile('^[#](\w+)$')
#     if not reg.match(value) :
#         raise ValidationError(u'%s hashtag doesnot comply' % value

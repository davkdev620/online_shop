from django import forms


# Form that used for the user to enter a coupon code.
class CouponApplyForm(forms.Form):
    code = forms.CharField()

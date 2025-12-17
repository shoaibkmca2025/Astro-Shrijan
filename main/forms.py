from django import forms

class BookingForm(forms.Form):
    service = forms.CharField(max_length=120)
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    dob = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    place = forms.CharField(max_length=200, required=False)
    questions = forms.CharField(widget=forms.Textarea, required=False)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number")
        return digits

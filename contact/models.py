from django import forms


class ContactForm(forms.Form):
    """
        A user can contact the admin via this form.
    """

    name = forms.CharField(
        max_length=256,
        help_text="Add your name.",
        label="Your name"
    )

    email = forms.EmailField(help_text="Add your email address.",
                             label="Your email address")

    subject = forms.CharField(max_length=256,
                              required=False,
                              help_text="Add your subject.",
                              label="The subject")

    message = forms.CharField(max_length=1024,
                              help_text="Your message.",
                              widget=forms.Textarea,
                              label="The message")

    spam = forms.CharField(max_length=0,
                           help_text='This should never be filled out!',
                           required=False,
                           label="A very basic spam filter",
                           widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')
        spam = cleaned_data.get('spam')
        if spam:
            raise forms.ValidationError("No robots (or spam) allowed here!")
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
